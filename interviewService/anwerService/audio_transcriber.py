import os
from groq import Groq
from utils.apierror import APIError

class AudioTranscriber:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        
    def transcribe_audio(self, audio_file_path: str) -> str:
        """Sends the webm audio file to Groq Whisper for lightning-fast transcription."""
        try:
            with open(audio_file_path, "rb") as file:
                transcription = self.client.audio.transcriptions.create(
                  file=(os.path.basename(audio_file_path), file.read()),
                  model="whisper-large-v3-turbo",
                  response_format="json",
                )
            return transcription.text
        except Exception as e:
            raise APIError(
                status_code=500, 
                message=f"Failed to transcribe: {str(e)}", 
                error_code="TRANSCRIPTION_FAILED"
            )