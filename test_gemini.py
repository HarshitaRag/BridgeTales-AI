# test_gemini.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

prompt = "A colorful children's storybook illustration about kindness, showing a young girl helping an elderly woman with groceries."

try:
    result = genai.generate_images(model="imagen-3.0", prompt=prompt)
    for img in result.images:
        print("✅ Image URL:", img.url)
except Exception as e:
    print("❌ Gemini error:", e)