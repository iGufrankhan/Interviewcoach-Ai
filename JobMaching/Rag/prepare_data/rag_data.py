import hashlib
import json
import os
import time
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from utils.apierror import APIError
from utils.constant import (EMBEDDING_MODEL, HF_TOKEN, RAG_CHUNK_SIZE, RAG_CHUNK_OVERLAP, RAG_RETRIEVER_K,CACHE_TTL)


from huggingface_hub import InferenceClient

class HFEmbeddingAPI:
    def __init__(self, token):
        self.client = InferenceClient(token=token)
        self.model = EMBEDDING_MODEL

    def embed_documents(self, texts):
        return self.client.feature_extraction(
            model=self.model,
            inputs=texts
        )

    def embed_query(self, text):
        return self.client.feature_extraction(
            model=self.model,
            inputs=[text]
        )[0]



class RagData:
    # Cache with TTL: {hash: (retriever, timestamp)}
    _cache = {}
    """
    Data preparation for RAG-based job matching analysis
    - Caches FAISS retrievers with 1-hour TTL
    - Automatic expiration prevents stale embeddings
    """
    
    def __init__(self, job_description: str, resume_data: dict = None):
        self.job_description = job_description
        self.resume_data = resume_data or {}
        self.embeddings = HFEmbeddingAPI(HF_TOKEN)
    
    @classmethod
    def _is_cache_expired(cls, cache_entry: tuple) -> bool:
        """Check if cache entry has expired
        
        Args:
            cache_entry: (retriever, timestamp) tuple
            
        Returns:
            True if expired, False if still valid
        """
        if cache_entry is None:
            return True
        
        retriever, timestamp = cache_entry
        elapsed_seconds = time.time() - timestamp
        
        if elapsed_seconds > CACHE_TTL:
            print(f"[RAG] Cache expired after {elapsed_seconds:.0f}s (TTL: {CACHE_TTL}s)")
            return True
        
        return False
    
    @classmethod
    def _cleanup_expired_cache(cls):
        """Remove expired entries from cache
        
        Run periodically to prevent memory buildup
        """
        current_time = time.time()
        expired_keys = []
        
        for cache_hash, cache_entry in cls._cache.items():
            _, timestamp = cache_entry
            if current_time - timestamp > CACHE_TTL:
                expired_keys.append(cache_hash)
        
        for cache_hash in expired_keys:
            del cls._cache[cache_hash]
            print(f"[RAG] Removed expired cache entry: {cache_hash}")
        
        if expired_keys:
            print(f"[RAG] Cleanup: Removed {len(expired_keys)} expired entries. Cache size now: {len(cls._cache)}")
    
    def prepare_for_rag(self):
        """
        Prepare resume data for RAG analysis with TTL caching
        
        Returns:
            FAISS retriever for semantic search
        """
        try:
            # Create stable hash of resume data
            resume_json = json.dumps(self.resume_data, sort_keys=True, default=str)
            resume_hash = hashlib.md5(resume_json.encode()).hexdigest()
            
            # Check if cached AND not expired
            if resume_hash in self._cache:
                cache_entry = self._cache[resume_hash]
                
                if not self._is_cache_expired(cache_entry):
                    retriever, timestamp = cache_entry
                    age_seconds = time.time() - timestamp
                    print(f"[RAG] Cache HIT for resume hash: {resume_hash} (age: {age_seconds:.0f}s)")
                    return retriever
                else:
                    # Cache expired, remove it
                    del self._cache[resume_hash]
                    print(f"[RAG] Cache EXPIRED for resume hash: {resume_hash}")
            
            # Periodically clean up expired entries
            if len(self._cache) % 10 == 0:  # Every 10 new entries
                self._cleanup_expired_cache()
            
            # Cache miss or expired - create new embeddings
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=RAG_CHUNK_SIZE,
                chunk_overlap=RAG_CHUNK_OVERLAP,
                separators=["\n\n", "\n", ". ", " ", ""]
            )
            
            documents = []
            
            if self.resume_data:
                resume_text = self._format_resume_text()
                resume_doc = Document(
                    page_content=f"Resume: {resume_text}",
                    metadata={"source": "resume", "type": "resume"}
                )
                resume_chunks = text_splitter.split_documents([resume_doc])
                documents.extend(resume_chunks)
            
            if not documents:
                raise APIError(
                    status_code=400,
                    message="No resume documents to process",
                    error_code="NO_RESUME_DATA"
                )
            
            # Create FAISS vector store
            vector_store = FAISS.from_documents(
                documents=documents,
                embedding=self.embeddings
            )
            
            retriever = vector_store.as_retriever(search_kwargs={"k": RAG_RETRIEVER_K})
            
            self._cache[resume_hash] = (retriever, time.time())
            print(f"[RAG] Cached FAISS index for resume hash: {resume_hash} (TTL: {CACHE_TTL}s). Cache size: {len(self._cache)}")
            
            return retriever
            
        except Exception as e:
            raise APIError(
                status_code=500,
                message=f"Failed to prepare RAG data: {str(e)}",
                error_code="RAG_PREPARATION_FAILED"
            )
    
    def _format_resume_text(self) -> str:
        """Format resume data into readable text"""
        text_parts = []
        
        if self.resume_data.get("name"):
            text_parts.append(f"Name: {self.resume_data['name']}")
        
        if self.resume_data.get("skills"):
            text_parts.append(f"Skills: {', '.join(self.resume_data['skills'])}")
        
        if self.resume_data.get("experience"):
            experience = self.resume_data['experience']
            if isinstance(experience, list):
                text_parts.append(f"Experience: {' '.join(experience)}")
            else:
                text_parts.append(f"Experience: {experience}")
        
        if self.resume_data.get("education"):
            education = self.resume_data['education']
            if isinstance(education, list):
                text_parts.append(f"Education: {' '.join(education)}")
            else:
                text_parts.append(f"Education: {education}")
        
        if self.resume_data.get("projects"):
            projects = self.resume_data['projects']
            if isinstance(projects, list):
                text_parts.append(f"Projects: {' '.join(projects)}")
            else:
                text_parts.append(f"Projects: {projects}")
        
        return "\n".join(text_parts)
    
    @classmethod
    def get_cache_status(cls):
        """Get cache status for monitoring"""
        current_time = time.time()
        cache_info = {
            "total_cached": len(cls._cache),
            "entries": []
        }
        
        for cache_hash, cache_entry in cls._cache.items():
            _, timestamp = cache_entry
            age_seconds = current_time - timestamp
            is_expired = age_seconds > CACHE_TTL
            
            cache_info["entries"].append({
                "hash": cache_hash,
                "age_seconds": f"{age_seconds:.0f}",
                "expired": is_expired,
                "ttl_remaining": f"{max(0, CACHE_TTL - age_seconds):.0f}"
            })
        
        return cache_info
    
    @classmethod
    def clear_cache(cls):
        """Clear all cached retrievers"""
        cls._cache.clear()
        print("[RAG] Cache cleared successfully")
    
    @classmethod
    def force_refresh_cache(cls, resume_hash: str = None):
        """Force refresh specific cache entry or all entries
        
        Args:
            resume_hash: Specific hash to refresh, or None for all
        """
        if resume_hash and resume_hash in cls._cache:
            del cls._cache[resume_hash]
            print(f"[RAG] Forced refresh for hash: {resume_hash}")
        elif resume_hash is None:
            cls._cache.clear()
            print("[RAG] Forced refresh: Cleared all cached entries")









