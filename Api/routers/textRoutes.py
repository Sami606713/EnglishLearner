from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from text.textCorrection import textCorrection
from text.languageLearner import learningAgent
from audio.voicePronunciation import speech_to_text
from image.imageToText import extract_text_from_image
from fastapi.responses import FileResponse
from schema.schema import Text
from gtts import gTTS
import tempfile
import shutil
import os

routes = APIRouter(
    prefix="/text",
    tags=["Text"]
)

@routes.post("/correct")
def CorrectText(data: Text):
    """
    Corrects the text
    """
    try:
        text = data.text
        response = textCorrection(text)
        return {"text": text, "corrected_text": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@routes.post("/learn")
def LearnEnglish(data: Text):
    """
    Learn English
    """
    try:
        query = data.text
        response = learningAgent(query)
        return {"query": query, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@routes.post("/ocr-text-correction")
async def CorrectOCRText(file: UploadFile = File(...)):
    try:
        temp_dir = tempfile.mkdtemp()

        # Handle missing extension
        ext_map = {
            "image/png": ".png",
            "image/jpeg": ".jpg",
            "image/jpg": ".jpg",
            "image/bmp": ".bmp",
            "image/gif": ".gif",
            "image/tiff": ".tiff",
            "application/pdf": ".pdf"
        }

        filename = file.filename or "uploaded_file"
        ext = os.path.splitext(filename)[1].lower()
        if not ext:
            ext = ext_map.get(file.content_type, "")
            filename += ext
        
        temp_file_path = os.path.join(temp_dir, filename)

        # Save uploaded file
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # OCR
        extracted_text = extract_text_from_image(temp_file_path)

        # Correction
        corrected_text = textCorrection(extracted_text)
        
        # Cleanup
        os.remove(temp_file_path)
        os.rmdir(temp_dir)

        return {"filename": filename, "extracted_text": extracted_text, "corrected_text": corrected_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@routes.post("/voice-pronunciation-correction")
async def correct_voice_pronunciation(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.wav'):
        raise HTTPException(status_code=400, detail="Only .wav audio files are accepted.")
    
    if file.content_type != "audio/wav":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a WAV audio file.")

    temp_audio_path = None
    temp_speech_path = None

    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            shutil.copyfileobj(file.file, temp_audio)
            temp_audio_path = temp_audio.name

        # Convert speech to text
        transcribed_text = speech_to_text(temp_audio_path)

        if not transcribed_text:
            raise HTTPException(status_code=400, detail="Speech recognition failed or no speech detected.")

        # Correct the transcribed text
        corrected_text = textCorrection(transcribed_text)
        print(corrected_text)
        # Convert corrected text to speech using gTTS
        tts = gTTS(corrected_text, lang="en")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_speech_file:
            tts.save(temp_speech_file.name)
            temp_speech_path = temp_speech_file.name

        # Return the full mp3 file
        return FileResponse(temp_speech_path, media_type="audio/mpeg", filename="corrected_speech.mp3")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    finally:
        # Clean up the input file only
        if temp_audio_path and os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
        # DO NOT delete temp_speech_path here if you're returning it; let FastAPI serve it first.
