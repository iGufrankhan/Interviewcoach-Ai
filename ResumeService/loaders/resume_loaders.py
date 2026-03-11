from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader

from ResumeService.utils.file_validators import validate_file_extension, validate_file_size, validate_not_empty
from utils.apierror import APIError


class ResumeLoader:

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_resume(self) -> str:
        # validate the file
        if not validate_file_extension(self.file_path):
            raise APIError(status_code=400, message="Invalid file type. Allowed types are: pdf, docx, txt", error_code="INVALID_FILE_TYPE")

        if not validate_file_size(self.file_path):
            raise APIError(status_code=400, message="File size exceeds the maximum limit of 5 MB", error_code="FILE_SIZE_EXCEEDED")

        if not validate_not_empty(self.file_path):
            raise APIError(status_code=400, message="File is empty", error_code="EMPTY_FILE")

        loader = self.get_loader()
        documents = loader.load()

        if not documents:
            raise APIError(status_code=400, message="Failed to extract text from the file", error_code="TEXT_EXTRACTION_FAILED")
        return documents[0].page_content

    def get_loader(self):
        ext = self.file_path.rsplit('.', 1)[1].lower()
        if ext == 'pdf':
            return PyPDFLoader(self.file_path)
        elif ext == 'docx':
            return Docx2txtLoader(self.file_path)
        elif ext == 'txt':
            return TextLoader(self.file_path)
        else:
            raise APIError(status_code=400, message="Unsupported file type", error_code="UNSUPPORTED_FILE_TYPE")









