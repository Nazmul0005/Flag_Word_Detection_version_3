#Import keys
from com.mhire.app.data.audio_path import audio_path
from com.mhire.app.services.transcribe import transcribe_audio
from com.mhire.app.services.detection import moderate_text

transcribed_text = transcribe_audio(audio_path)
print("Transcription:", transcribed_text)


# Returns moderation results

# Example usage
moderation_result = moderate_text(transcribed_text)
if moderation_result.flagged:
    print("⚠️ Inappropriate content detected!")
    print("Categories flagged:", moderation_result.categories)
else:
    print("✅ Content is clean.")

