import os
from google import genai

def get_ai_response(prompt: str):
    # Initialising the Gemini client with the API key from environment variables
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    # using gemini model
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
    )
    
    return response.text