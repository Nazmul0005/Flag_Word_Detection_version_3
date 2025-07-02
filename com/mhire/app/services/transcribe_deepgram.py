import requests
import os
from com.mhire.app.config.config import DEEPGRAM_API_KEY

def transcribe_audio_deepgram(audio_file_path):
    """
    Transcribe audio using Deepgram Nova-2 API
    """
    url = "https://api.deepgram.com/v1/listen"
    
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "audio/wav"  # Adjust based on your audio format
    }
    
    params = {
        "model": "nova-2",
        "smart_format": "true",
        "punctuate": "true",
        "diarize": "true",
        "language": "en"
    }
    
    try:
        with open(audio_file_path, "rb") as audio_file:
            response = requests.post(
                url,
                headers=headers,
                params=params,
                data=audio_file
            )
        
        if response.status_code == 200:
            result = response.json()
            # Extract transcript from Deepgram response
            transcript = result["results"]["channels"][0]["alternatives"][0]["transcript"]
            return transcript
        else:
            raise Exception(f"Deepgram API error: {response.status_code} - {response.text}")
            
    except Exception as e:
        raise Exception(f"Error transcribing with Deepgram: {str(e)}")