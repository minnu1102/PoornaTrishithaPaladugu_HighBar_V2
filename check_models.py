import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("No API Key found in .env")
else:
    genai.configure(api_key=api_key)
    print(" Checking available models for your key...\n")
    try:
        # List all models available to your API key
        for m in genai.list_models():
            # Check if the model supports content generation
            if 'generateContent' in m.supported_generation_methods:
                print(f"Available: {m.name}")
    except Exception as e:
        print(f" Error: {e}")