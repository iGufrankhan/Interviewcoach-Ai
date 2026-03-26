
import hashlib
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from utils.apierror import APIError

# Configuration constants
RAG_CHUNK_SIZE = 500
RAG_CHUNK_OVERLAP = 100
RAG_RETRIEVER_K = 5  # Number of similar chunks to retrieve
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


class RagData:
    # Class-level cache for FAISS retrievers - prevents re-embedding same resumes
    _cache = {}
    """
    Data preparation for RAG-based job matching analysis
    - Loads and processes resume and job description data
    - Supports both LLM-only and Hybrid RAG modes
    - Handles errors gracefully with detailed logging
    """
    
    def __init__(self, job_description: str, resume_data: dict = None):
        """
        Initialize RAG data processor
        
        Args:
            job_description: Job description text
            resume_data: Resume data dictionary
        """
        self.job_description = job_description
        self.resume_data = resume_data or {}
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        
        
    def prepare_for_rag(self):
        """
        Prepare resume data for RAG analysis
        - Chunks resume data as documents
        - Creates vector embeddings using HuggingFace models
        - Stores ONLY resume documents in FAISS vector DB
        - Job description is used during LLM comparison, not in FAISS
        - CACHES retrieved to avoid re-embedding same resume multiple times
        
        Returns:
            FAISS retriever for semantic search on resume data
        """
        try:
            # Create hash of resume data for caching
            resume_hash = hashlib.md5(str(self.resume_data).encode()).hexdigest()
            
            # Check if already computed and cached
            if resume_hash in self._cache:
                return self._cache[resume_hash]
            
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
            
           
            vector_store = FAISS.from_documents(
                documents=documents,
                embedding=self.embeddings
            )
            
            retriever = vector_store.as_retriever(search_kwargs={"k": RAG_RETRIEVER_K})
            
            # Cache the retriever for future use
            self._cache[resume_hash] = retriever
            
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
        
        
        
            
            
            

    
    
    