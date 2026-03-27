import io
import base64
import wave
import speech_recognition as sr
from utils.apierror import APIError


class AudioTranscriber:
    """Transcribe audio files to text using Google Speech-to-Text API"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.recognizer = sr.Recognizer()
    
    def transcribe_audio(self, audio_data):
        """
        Transcribe audio blob/base64 to text
        
        Args:
            audio_data: base64 encoded audio string (WAV format)
            
        Returns:
            Transcribed text (str)
        """
        try:
            # Decode base64 to audio bytes
            if isinstance(audio_data, str):
                # Remove data URI prefix if present
                if audio_data.startswith('data:audio'):
                    audio_data = audio_data.split(',')[1]
                
                # Decode base64
                audio_bytes = base64.b64decode(audio_data)
            else:
                audio_bytes = audio_data
            
            if not audio_bytes:
                raise APIError(
                    status_code=400,
                    message="No audio data received",
                    error_code="EMPTY_AUDIO"
                )
            
            # Load audio from bytes
            try:
                audio_file = io.BytesIO(audio_bytes)
                
                # Try to use the audio file with speech_recognition
                with sr.AudioFile(audio_file) as source:
                    audio_content = self.recognizer.record(source)
                    
                    try:
                        # Use Google Speech Recognition
                        text = self.recognizer.recognize_google(audio_content, language='en-US')
                        return text
                    except sr.UnknownValueError:
                        raise APIError(
                            status_code=400,
                            message="Could not understand audio. Please speak clearly and try again.",
                            error_code="AUDIO_NOT_RECOGNIZED"
                        )
                    except sr.RequestError as e:
                        # Network or API error
                        raise APIError(
                            status_code=503,
                            message="Speech recognition service unavailable. Please try again or use text input.",
                            error_code="SPEECH_SERVICE_ERROR"
                        )
            except sr.UnknownValueError:
                raise APIError(
                    status_code=400,
                    message="Could not understand audio. Please speak clearly and try again.",
                    error_code="AUDIO_NOT_RECOGNIZED"
                )
            except sr.RequestError as e:
                raise APIError(
                    status_code=503,
                    message="Speech recognition service unavailable. Please check your internet connection.",
                    error_code="SPEECH_SERVICE_ERROR"
                )
            except Exception as format_error:
                raise APIError(
                    status_code=400,
                    message="Invalid audio format. Please ensure audio is in WAV format.",
                    error_code="INVALID_AUDIO_FORMAT"
                )
        
        except APIError:
            raise
        except Exception as e:
            raise APIError(
                status_code=500,
                message="Audio transcription failed. Please try again or use text input.",
                error_code="TRANSCRIPTION_FAILED"
            )
