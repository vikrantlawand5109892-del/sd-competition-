# gemini_client.py
import google.generativeai as genai

# Replace with your actual API key
GEMINI_API_KEY = "YOUR_API_KEY_HERE"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"
