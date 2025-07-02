from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from com.mhire.app.services.multi_provider_transcribe import transcribe_with_provider
from com.mhire.app.services.detection import moderate_text
import shutil
import tempfile
import os
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Voice Content Moderation API - Multi Provider",
    description="AI-powered content moderation for voice dating app with multiple transcription providers",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure with your frontend domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/transcribe")
def transcribe_endpoint(file: UploadFile = File(...), provider: str = Form("openai_whisper")):
    """
    Transcribe audio using the specified provider
    """
    try:
        logger.info(f"Transcribing with provider: {provider}")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
        
        transcript = transcribe_with_provider(tmp_path, provider)
        
        # Clean up temporary file
        os.unlink(tmp_path)
        
        return {"transcription": transcript, "provider_used": provider}
    except Exception as e:
        logger.error(f"Error transcribing with {provider}: {str(e)}")
        if 'tmp_path' in locals():
            try:
                os.unlink(tmp_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/moderate")
def moderate_endpoint(text: str):
    """
    Moderate text content
    """
    try:
        result = moderate_text(text)
        return JSONResponse(content={
            "flagged": result.flagged,
            "categories": dict(result.categories),
            "category_scores": dict(result.category_scores)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transcribe-and-moderate")
def transcribe_and_moderate_endpoint(file: UploadFile = File(...), provider: str = Form("openai_whisper")):
    """
    Main endpoint for voice dating app content moderation with provider selection.
    Returns transcription and moderation results for backend decision making.
    """
    try:
        logger.info(f"Processing audio file: {file.filename} with provider: {provider}")
        start_time = time.time()
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
        
        # Transcribe audio with selected provider
        transcript = transcribe_with_provider(tmp_path, provider)
        transcription_time = time.time() - start_time
        logger.info(f"Transcription completed in {transcription_time:.2f}s: {len(transcript)} characters")
        
        # Moderate content
        moderation_start = time.time()
        moderation_result = moderate_text(transcript)
        moderation_time = time.time() - moderation_start
        
        # Clean up temporary file
        os.unlink(tmp_path)
        
        total_time = time.time() - start_time
        
        # Structure response for backend decision making
        response = {
            "transcription": transcript,
            "moderation": {
                "flagged": moderation_result.flagged,
                "categories": dict(moderation_result.categories),
                "category_scores": dict(moderation_result.category_scores)
            },
            "recommendation": "block" if moderation_result.flagged else "allow",
            "provider_used": provider,
            "performance": {
                "total_time": round(total_time, 2),
                "transcription_time": round(transcription_time, 2),
                "moderation_time": round(moderation_time, 2)
            }
        }
        
        logger.info(f"Processing completed in {total_time:.2f}s - Result: {'FLAGGED' if moderation_result.flagged else 'CLEAN'}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing audio with {provider}: {str(e)}")
        # Clean up temp file if it exists
        if 'tmp_path' in locals():
            try:
                os.unlink(tmp_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "voice-moderation-multi-provider"}

@app.get("/providers")
def list_providers():
    """List available transcription providers"""
    return {
        "providers": [
            {
                "id": "openai_whisper",
                "name": "OpenAI Whisper",
                "description": "Industry standard, reliable transcription",
                "features": ["Multilingual", "Robust", "Widely used"]
            },
            {
                "id": "deepgram_nova_2",
                "name": "Deepgram Nova-2",
                "description": "Fastest, most accurate transcription",
                "features": ["Real-time streaming", "Speaker diarization", "36% better than Whisper"]
            },
            {
                "id": "groq_whisper_turbo",
                "name": "Groq Whisper Turbo",
                "description": "Ultra-fast processing, cost-effective",
                "features": ["Lightning fast", "Very cheap", "Good for high volume"]
            }
        ]
    }