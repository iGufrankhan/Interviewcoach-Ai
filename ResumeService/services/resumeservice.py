import os
import logging
from ResumeService.loaders.resume_loaders import ResumeLoader
from ResumeService.preprocessing.preprocessing import TextPreprocessor
from ResumeService.analyzer.analysis import ResumeAnalyzer
from ResumeService.repository.resume_datasave import save_resume
from utils.apierror import APIError
from Models.userReg.user import User

logger = logging.getLogger(__name__)


class ResumeService:

    def __init__(self, upload_dir: str, groq_api_key: str, user_id: str):
        logger.info(f"🔧 ResumeService init - user_id (email): {user_id}")
        
        # user_id is now the email (from JWT token)
        user_obj = User.objects(email=user_id).first()
        if not user_obj:
            logger.error(f"❌ User not found: {user_id}")
            raise APIError(status_code=404, message=f"User with email {user_id} not found", error_code="USER_NOT_FOUND")
        
        logger.info(f"✅ User found: {user_obj.email}")
        
        if not groq_api_key:
            logger.error("❌ GROQ API key is missing")
            raise APIError(status_code=400, message="GROQ API key is required", error_code="MISSING_API_KEY")
        
        self.upload_dir = upload_dir
        self.analyzer = ResumeAnalyzer(api_key=groq_api_key)
        self.user_id = user_id
        
        logger.info("✅ ResumeAnalyzer initialized")

        os.makedirs(self.upload_dir, exist_ok=True)
        logger.info(f"✅ Upload directory ready: {self.upload_dir}")

    def process_resume(self, file):
        logger.info(f"📄 Processing resume: {file.filename}")

        # 1️⃣ Save uploaded file
        file_path = os.path.join(self.upload_dir, file.filename)
        logger.info(f"💾 Saving file to: {file_path}")

        try:
            with open(file_path, "wb") as f:
                f.write(file.file.read())
            logger.info(f"✅ File saved successfully")
        except Exception as e:
            logger.error(f"❌ Failed to save file: {str(e)}", exc_info=True)
            raise

        # 2️⃣ Load resume text
        logger.info("📖 Loading resume text...")
        try:
            loader = ResumeLoader(file_path)
            raw_text = loader.load_resume()
            logger.info(f"✅ Resume text loaded. Length: {len(raw_text)} chars")
        except Exception as e:
            logger.error(f"❌ Failed to load resume: {str(e)}", exc_info=True)
            raise

        # 3️⃣ Preprocess text
        logger.info("🔤 Preprocessing text...")
        try:
            preprocessor = TextPreprocessor(raw_text)
            cleaned_text = preprocessor.preprocess()
            logger.info(f"✅ Text preprocessed. Length: {len(cleaned_text)} chars")
        except Exception as e:
            logger.error(f"❌ Failed to preprocess text: {str(e)}", exc_info=True)
            raise

        # 4️⃣ Analyze resume using LLM
        logger.info("🤖 Analyzing resume with Groq LLM...")
        try:
            structured_data = self.analyzer.analyze(cleaned_text)
            logger.info(f"✅ Resume analyzed successfully")
            logger.debug(f"   Data keys: {structured_data.keys() if isinstance(structured_data, dict) else 'N/A'}")
        except Exception as e:
            logger.error(f"❌ Failed to analyze resume: {str(e)}", exc_info=True)
            raise

        # 5️⃣ Save structured resume data
        logger.info("📊 Saving structured resume data...")
        try:
            saved_resume = save_resume(structured_data, self.user_id)
            logger.info(f"✅ Resume saved to database")
            return saved_resume
        except Exception as e:
            logger.error(f"❌ Failed to save resume to database: {str(e)}", exc_info=True)
            raise