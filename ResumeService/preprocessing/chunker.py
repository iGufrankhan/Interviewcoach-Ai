from langchain_text_splitters import RecursiveCharacterTextSplitter


class Chunker:
    
    def __init__(self, text: str, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.text = text
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    
    def split_into_chunks(self) -> list:
        """
        Split the input text into chunks using RecursiveCharacterTextSplitter.
        """
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        chunks = text_splitter.split_text(self.text)
        return chunks
    