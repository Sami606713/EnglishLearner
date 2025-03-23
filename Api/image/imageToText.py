import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

def extract_text_from_image(image_path):
    """
    Extracts text from an image using Google GenAI Gemini API.
    """
    # Initialize GenAI client
    client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

    # Upload image to GenAI files
    files = [
        client.files.upload(file=image_path),
    ]

    # Prepare content with uploaded image and extraction instruction
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_uri(
                    file_uri=files[0].uri,
                    mime_type=files[0].mime_type,
                ),
                types.Part.from_text(text="Please extract the text from this image."),
            ],
        ),
    ]

    # Set generation config
    generate_content_config = types.GenerateContentConfig(
        temperature=0,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="application/json",
        system_instruction=[
            types.Part.from_text(
                text="You are a helpful assistant responsible for extracting the text from the image. Respond with ONLY the extracted text and nothing else."
            ),
        ],
    )

    extracted_text = ""
    for chunk in client.models.generate_content_stream(
        model="gemini-2.0-flash",
        contents=contents,
        config=generate_content_config,
    ):
        extracted_text += chunk.text

    return extracted_text


if __name__ == "__main__":
    # Example usage
    image_path = "data/my_wallet.PNG"  # Make sure this path is correct
    text = extract_text_from_image(image_path)
    print(text)
