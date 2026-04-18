from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def route_with_gemini(user_input: str):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Classify into: task, calendar, notes, data\nInput: {user_input}"
    )
    
    return response.text.strip().lower()