import requests
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OCR_SPACE_API_KEY")

def extract_text_from_image(image_path):
    """
    Extracts text from an image using OCR.Space API.

    :param image_path: Path to the image file
    :return: Extracted text or an error message
    """
    if not API_KEY:
        return "Error: API Key not found in environment variables."

    with open(image_path, "rb") as image_file:
        response = requests.post(
            "https://api.ocr.space/parse/image",
            files={"file": image_file},
            data={"apikey": API_KEY, "language": "eng"}
        )

    result = response.json()

    if "ParsedResults" in result:
        return result["ParsedResults"][0]["ParsedText"]
    else:
        return f"Error: {result.get('ErrorMessage', 'Unknown error')}"


if __name__=="__main__":
    # Example usage
    image_path = "data/my_wallet.PNG"
    text = extract_text_from_image(image_path)
    print(text)
