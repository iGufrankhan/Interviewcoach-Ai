from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from utils.apierror import APIError


class JobDescriptionLoader:

    def load_job_description(self, description: str) -> str:
        return description.lower()

    def load_job_description_from_url(self, url: str, api_key: str) -> str:
        try:
            loader = WebBaseLoader(url)
            documents = loader.load()

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=800,
                chunk_overlap=100
            )

            chunks = splitter.split_documents(documents)

            if not chunks:
                raise APIError(
                    status_code=400,
                    message="Failed to split job description",
                    error_code="TEXT_SPLITTING_FAILED"
                )

            
            chunks = chunks[:3]

            extracted_parts = []

            prompt_template = PromptTemplate(
                input_variables=["chunk"],
                template="""
Extract only important job information:

- role
- required skills
- experience
- responsibilities

Return clean text only.

Job Text:
{chunk}
"""
            )
            
            llm = ChatGroq(
                model_name="llama-3.1-8b-instant",
                groq_api_key=api_key,
                temperature=0
            )

            for chunk in chunks:
                prompt = prompt_template.format(chunk=chunk.page_content[:1500])

                response = llm.invoke(prompt)

                extracted_parts.append(response.content.strip())

            final_text = "\n".join(extracted_parts)

            if not final_text:
                raise APIError(
                    status_code=400,
                    message="Failed to extract job content",
                    error_code="TEXT_EXTRACTION_FAILED"
                )

            return final_text

        except Exception as e:
            raise APIError(
                status_code=400,
                message=str(e),
                error_code="URL_LOADING_FAILED"
            )