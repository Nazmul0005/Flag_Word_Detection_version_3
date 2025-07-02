from com.mhire.app.services.transcribe import transcribe_audio
from com.mhire.app.services.transcribe_deepgram import transcribe_audio_deepgram
from com.mhire.app.services.transcribe_groq import transcribe_audio_groq

def transcribe_with_provider(audio_file_path, provider="openai_whisper"):
    """
    Transcribe audio using the specified provider
    
    Args:
        audio_file_path (str): Path to the audio file
        provider (str): Provider to use ("openai_whisper", "deepgram_nova-2", "groq_whisper_turbo")
    
    Returns:
        str: Transcribed text
    """
    
    provider = provider.lower().replace(" ", "_").replace("-", "_")
    
    if provider == "openai_whisper":
        return transcribe_audio(audio_file_path)
    elif provider == "deepgram_nova_2":
        return transcribe_audio_deepgram(audio_file_path)
    elif provider == "groq_whisper_turbo":
        return transcribe_audio_groq(audio_file_path)
    else:
        # Default to OpenAI if provider not recognized
        return transcribe_audio(audio_file_path)