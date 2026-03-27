import speech_recognition as sr
from utils.apierror import APIError

class AnwerListen:
    def __init__(self):
        self.recognizer = sr.Recognizer()
       

    def listen(self):
        """Listen to audio and convert to text with fallback"""
        with sr.Microphone() as source:
            print("Listening for answer...")
            try:
                audio = self.recognizer.listen(source, timeout=30)
            except sr.RequestError as e:
                raise APIError(
                    status_code=500,
                    message=f"Microphone error: {e}",
                    error_code="MICROPHONE_ERROR"
                )

        try:
            text = self.recognizer.recognize_google(audio)
            return text
           
        except sr.UnknownValueError:
            raise APIError(
                status_code=400,
                message="Could not understand audio. Please try again or type your answer.",
                error_code="AUDIO_NOT_RECOGNIZED"
            )
        except sr.RequestError as e:
            raise APIError(
                status_code=503,
                message=f"Speech recognition service unavailable: {e}. Please use text input.",
                error_code="SPEECH_SERVICE_UNAVAILABLE"
            )
        

        
        
        