from fastapi import APIRouter, UploadFile, File, HTTPException
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
    """
    Handles OCR text correction from an uploaded audio file.
    """
    try:
        # Save the uploaded file to a temporary location
        temp_dir = tempfile.mkdtemp()
        temp_file_path = os.path.join(temp_dir, file.filename)
        
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Perform OCR
        extracted_text = extract_text_from_image(temp_file_path)

        # Correct the extracted text
        corrected_text = textCorrection(extracted_text)
        
        # Clean up temporary file
        os.remove(temp_file_path)
        os.rmdir(temp_dir)

        return {"filename": file.filename,"extracted_text":extracted_text, "corrected_text": corrected_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@routes.post("/voice-pronunciation-correction")
async def CorrectVoicePronunciation(file: UploadFile = File(...)):
    """
    Handles voice pronunciation correction and returns an audio response.
    """
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_audio:
            shutil.copyfileobj(file.file, temp_audio)
            temp_audio_path = temp_audio.name

        # Convert speech to text
        transcribed_text = speech_to_text(temp_audio_path)

        # Cleanup: Delete temp file after processing
        os.remove(temp_audio_path)

        if transcribed_text:
            # Correct the transcribed text
            corrected_text = textCorrection(transcribed_text)

            # Convert corrected text to speech using gTTS
            tts = gTTS(corrected_text, lang="en")
            temp_speech_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(temp_speech_file.name)

            return FileResponse(
                temp_speech_file.name,
                media_type="audio/mpeg",
                filename="corrected_speech.mp3"
            )
        else:
            raise HTTPException(status_code=400, detail="Speech recognition failed.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
