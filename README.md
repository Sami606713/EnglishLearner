# Text Correction API Documentation
## Overview
- The Text Correction API is a RESTful API built using FastAPI. It provides functionalities for:

    - Text correction.

    - English learning assistance.

    - OCR (Image to Text with Correction).

    - Voice pronunciation correction (Speech to text, correct it, then return audio).

# API Endpoints
## Base Route
`GET /`

- Returns a simple welcome message.

`Response:`

```json
"Welcome to the text correction API"
```

### 1. Correct Text
`POST /text/correct`

### Description:
- Corrects grammatical errors in the input text.
- We can use the `llama-3.1-8b-instant` model for text correction.

`Request:`
```json
{
    "text": "I a am boy"
}
```
`Response:`
```json
{
    "text": "I a am boy",
    "corrected_text": "I am a boy"
}
```
### 2. English Learning Agent
- `POST /text/learn`

### Description:
- An interactive agent that helps users learn English (e.g., roadmap, exercises).
- For English learning we can make the `agent` that can use the `llama-3.1-8b-instant` model and also have a memory mean that i can retain the previous knowladge.

`Request:`
```json
{
    "text": "I want to learn English"
}
```

`Response:`
```json
{
    "query": "I want to learn English",
    "response": "<learning roadmap or answer>"
}
```
### 3. OCR + Text Correction
- `POST /text/ocr-text-correction`

### Description:
- Uploads an image, extracts text using OCR (Google GenAI), and returns corrected text.
- For this we can use the two model.
    - `Google Gemeni` for text extraction.
    - `llama-3.1-8b-instant` for text correction.
 
`Request:`
- `file:` Upload an image file (png, jpg, jpeg, etc.)

`Response:`
```json
{
    "filename": "uploaded_file.jpg",
    "extracted_text": "Extracted text from image",
    "corrected_text": "Corrected extracted text"
}
```

### 4. Voice Pronunciation Correction
- `POST /text/voice-pronunciation-correction`

### Description:
- Uploads a .wav audio file, converts speech to text, corrects it, and returns corrected audio as an .mp3.
- For this we can you the `Speech Recognization Libraray` for converting audio to text.
- After converting the text we can pass the text to our text correction model to correct the text.
- After text is correct we can use the `Google Text to Speech` to convert the text to speech.

`Request:`
- `file:` Upload a .wav audio file.

`Response:`
- Returns an MP3 audio file stream containing corrected speech.


# Core Modules
`textCorrection.py`
- Loads a prompt template from correction.md.

- Uses Langchain to invoke a model and correct text.

`languageLearner.py`
- Creates an interactive agent for English learning.

- Stores memory of conversation using ConversationBufferMemory.

- imageToText.py
Extracts text from an image using Google GenAI Gemini API.

- Utilizes genai.Client to upload image and retrieve extracted text.

`voicePronunciation.py`
- Converts speech to text using the SpeechRecognition library.

- Supports only .wav audio files.

## API Endpoints and Model Usage

| Feature                        | Model Used                          | Endpoint                                | Input Format                              | Response Format                              |
|---------------------------------|------------------------------------|-----------------------------------------|------------------------------------------|--------------------------------------------|
| **Text Correction**             | `llama-3.1-8b-instant`            | `POST /text/correct`                    | `{ "text": "I a am boy" }`               | `{ "text": "I a am boy", "corrected_text": "I am a boy" }` |
| **English Learning Agent**      | `llama-3.1-8b-instant` (with memory) | `POST /text/learn`                      | `{ "text": "I want to learn English" }`  | `{ "query": "I want to learn English", "response": "<learning roadmap or answer>" }` |
| **OCR + Text Correction**       | `Google Gemini` (OCR) + `llama-3.1-8b-instant` (Correction) | `POST /text/ocr-text-correction` | `file: image (png, jpg, jpeg, etc.)`     | `{ "filename": "uploaded_file.jpg", "extracted_text": "Extracted text from image", "corrected_text": "Corrected extracted text" }` |
| **Voice Pronunciation Correction** | `SpeechRecognition` (Speech-to-Text) + `llama-3.1-8b-instant` (Correction) + `Google Text-to-Speech` (Text-to-Speech) | `POST /text/voice-pronunciation-correction` | `file: audio (.wav)` | Returns corrected speech as an MP3 audio file |

## Core Modules

| Module Name               | Functionality |
|---------------------------|--------------|
| `textCorrection.py`       | Loads a prompt template from `correction.md` and uses Langchain to invoke a model for text correction. |
| `languageLearner.py`      | Creates an interactive agent for English learning with conversation memory. |
| `imageToText.py`         | Extracts text from an image using Google Gemini API. |
| `voicePronunciation.py`  | Converts speech to text using SpeechRecognition and generates corrected speech using Google Text-to-Speech (gTTS). |

## Technologies Used

# Technologies Used
- FastAPI (API framework)

- Langchain (LLM + Prompt Engineering)

- Google GenAI (OCR)

- SpeechRecognition (Speech-to-Text)

- gTTS (Google Text-to-Speech)

- uvicorn (ASGI server)

# Environment Variables
- You can get the api key here.
- [GENAI_API_KEY](https://aistudio.google.com/app/apikey)
- [Groq API](https://console.groq.com/keys?_gl=1*164s6bk*_ga*MTEwMDcwMjk1My4xNzQwNTA3ODkx*_ga_4TD0X2GEZG*MTc0Mjg5NDY2NC43LjAuMTc0Mjg5NDY2NC4wLjAuMA..)
```env
GROQ_API_KEY = <You Groq Api>

GENAI_API_KEY = <Your Google Genai APi>
```


# How To Run 
- For running the `API` must sure that you have docker install.v 
- If not install first. 
    - [docker](https://www.docker.com/products/docker-desktop/)
- After installing the docker now pull the docker image by running this command
```bash
docker pull sami606713/text_correction:latest
```

- After pulling the image run the image and make sure pass the API keys befire running the image.
```
docker run -p 8000:8000 -e GROQ_API_KEY=your_key -e GENAI_API_KEY=your_key sami606713/text_correction:latest
```

- After running the image now you can access the API in the browser.
```bash
http://localhost:8000/
```