import os
from ResumeService.loaders.resume_loaders import ResumeLoader
from ResumeService.preprocessing.preprocessing import TextPreprocessor
from ResumeService.analyzer.analysis import ResumeAnalyzer


class ResumeService:

    def __init__(self, upload_dir: str, groq_api_key: str):
        self.upload_dir = upload_dir
        self.analyzer = ResumeAnalyzer(api_key=groq_api_key)

        os.makedirs(self.upload_dir, exist_ok=True)

    def process_resume(self, file):

        # 1️⃣ Save uploaded file
        file_path = os.path.join(self.upload_dir, file.filename)

        with open(file_path, "wb") as f:
            f.write(file.file.read())

        # 2️⃣ Load resume text
        loader = ResumeLoader(file_path)
        raw_text = loader.load_resume()

        # 3️⃣ Preprocess text
        preprocessor = TextPreprocessor(raw_text)
        cleaned_text = preprocessor.preprocess()

        # 4️⃣ Analyze resume using LLM
        structured_data = self.analyzer.analyze(cleaned_text)

        # 5️⃣ Save structured resume data (TODO)
        # saved_resume = save_resume(structured_data)

        return structured_data