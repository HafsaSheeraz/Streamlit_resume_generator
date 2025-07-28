# test_api.py

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # Make sure .env has this key

model = genai.GenerativeModel("models/gemini-1.5-flash")  # Use correct model path

response = model.generate_content("Write a professional resume for a software engineer.")
print(response.text)
