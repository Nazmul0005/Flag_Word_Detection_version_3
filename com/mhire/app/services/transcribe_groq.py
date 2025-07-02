import requests
import os
from com.mhire.app.config.config import GROQ_API_KEY

def transcribe_audio_groq(audio_file_path):
    """
    Transcribe audio using Groq Whisper Turbo API
    """
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    
    try:
        with open(audio_file_path, "rb") as audio_file:
            files = {
                "file": (os.path.basename(audio_file_path), audio_file, "audio/mpeg"),
                "model": (None, "whisper-large-v3-turbo"),
                "response_format": (None, "json"),
                "language": (None, "en")
            }
            
            response = requests.post(url, headers=headers, files=files)
        
        if response.status_code == 200:
            result = response.json()
            return result["text"]
        else:
            raise Exception(f"Groq API error: {response.status_code} - {response.text}")
            
    except Exception as e:
        raise Exception(f"Error transcribing with Groq: {str(e)}")