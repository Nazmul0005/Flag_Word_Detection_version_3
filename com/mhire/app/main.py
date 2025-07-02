from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from com.mhire.app.services.transcribe import transcribe_audio
from com.mhire.app.services.detection import moderate_text
import shutil
import tempfile
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Voice Content Moderation API",
    description="AI-powered content moderation for voice dating app",
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
def transcribe_endpoint(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
        transcript = transcribe_audio(tmp_path)
        return {"transcription": transcript}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/moderate")
def moderate_endpoint(text: str):
    try:
        result = moderate_text(text)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transcribe-and-moderate")
def transcribe_and_moderate_endpoint(file: UploadFile = File(...)):
    """
    Main endpoint for voice dating app content moderation.
    Returns transcription and moderation results for backend decision making.
    """
    try:
        logger.info(f"Processing audio file: {file.filename}")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
        
        # Transcribe audio
        transcript = transcribe_audio(tmp_path)
        logger.info(f"Transcription completed: {len(transcript)} characters")
        
        # Moderate content
        moderation_result = moderate_text(transcript)
        
        # Clean up temporary file
        os.unlink(tmp_path)
        
        # Structure response for backend decision making
        response = {
            "transcription": transcript,
            "moderation": {
                "flagged": moderation_result.flagged,
                "categories": dict(moderation_result.categories),
                "category_scores": dict(moderation_result.category_scores)
            },
            "recommendation": "block" if moderation_result.flagged else "allow"
        }
        
        logger.info(f"Moderation result: {'FLAGGED' if moderation_result.flagged else 'CLEAN'}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}")
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
    return {"status": "healthy", "service": "voice-moderation"}
