import speech_recognition as sr

def speech_to_text(audio_file):
  """
  Converts speech from an audio file to text.

  Args:
    audio_file: Path to the audio file.

  Returns:
    The transcribed text, or None if an error occurs.
  """
  recognizer = sr.Recognizer()
  try:
    with sr.AudioFile(audio_file) as source:
      audio = recognizer.record(source)  # Read the entire audio file
    text = recognizer.recognize_google(audio)
    return text
  except sr.UnknownValueError:
    print("Speech Recognition could not understand audio")
    return None
  except sr.RequestError as e:
    print(f"Could not request results from Speech Recognition service; {e}")
    return None
  
if __name__ == "__main__":
    audio_file = "data/03-01-01-01-01-01-01.wav"
    text = speech_to_text(audio_file)
    print(text)