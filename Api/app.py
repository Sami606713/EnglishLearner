import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/text"  # Change this to your FastAPI server URL

st.title("Text Processing API Tester")

# Correct Text Endpoint
txt = st.text_area("Enter text for correction:")
if st.button("Correct Text"):
    response = requests.post(f"{API_URL}/correct", json={"text": txt})
    if response.status_code == 200:
        st.success(response.json()["corrected_text"])
    else:
        st.error("Error: " + response.json()["detail"])

# Learn English Endpoint
learn_txt = st.text_area("Enter text for learning assistance:")
if st.button("Learn English"):
    response = requests.post(f"{API_URL}/learn", json={"text": learn_txt})
    if response.status_code == 200:
        st.success(response.json()["response"])
    else:
        st.error("Error: " + response.json()["detail"])

# OCR Text Correction
uploaded_ocr_file = st.file_uploader("Upload an image for OCR-based correction", type=["png", "jpg", "jpeg"])
if uploaded_ocr_file and st.button("Correct OCR Text"):
    files = {"file": uploaded_ocr_file.getvalue()}
    response = requests.post(f"{API_URL}/ocr-text-correction", files=files)
    if response.status_code == 200:
        data = response.json()
        st.write("Extracted Text:", data["extracted_text"])
        st.success("Corrected Text: " + data["corrected_text"])
    else:
        st.error("Error: " + response.json()["detail"])

# Voice Pronunciation Correction
uploaded_audio_file = st.file_uploader("Upload an audio file for pronunciation correction", type=["wav", "mp3", "m4a"])
if uploaded_audio_file and st.button("Correct Voice Pronunciation"):
    files = {"file": uploaded_audio_file.getvalue()}
    response = requests.post(f"{API_URL}/voice-pronunciation-correction", files=files)
    if response.status_code == 200:
        st.audio(response.content)
    else:
        st.error("Error: " + response.json()["detail"])
