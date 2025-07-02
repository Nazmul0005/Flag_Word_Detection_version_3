#2. Transcribe Audio with Whisper API

# from config import OPENAI_API_KEY
# client = openai.OpenAI(api_key = OPENAI_API_KEY) 

from com.mhire.app.client.openai_client import client
def transcribe_audio(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
         )
    return transcript.text

