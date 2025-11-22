import google.generativeai as genai
import json
import re
from settings import GEMINI_API_KEY

# Configure the API
genai.configure(api_key=GEMINI_API_KEY)

def clean_json_text(text):
    """Clean up any Markdown wrapping (```json ... ```) that might appear."""
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*", "", text)
    return text.strip()

def extract_key_value_pairs(text):
    # ✅ CHANGE 1: Use the model we proved works for you
    model_name = "models/gemini-2.0-flash"

    try:
        model = genai.GenerativeModel(
            model_name,
            generation_config={"response_mime_type": "application/json"}
        )

        # ✅ CHANGE 2: Specific Prompt to match "Expected Output" format
        prompt = f"""
        You are an expert data extractor.
        
        Task:
        1. Extract ALL information from the text below into a JSON LIST.
        2. **Formatting Rules (Crucial):**
           - Split Person Names into two keys: "First Name" and "Last Name".
           - Split Locations into two keys: "Birth City" and "Birth State" (or similar).
           - For dates, use YYYY-MM-DD format if possible.
        
        3. **Context Rules (Comments):**
           - The "Comments" field must contain the **exact full sentence** from the text where the data was found.
           - Do not shorten or summarize the comment.
        
        4. Output must be a JSON list of objects with keys: "Key", "Value", "Comments".

        PDF TEXT:
        {text[:30000]}
        """

        print(f"🤖 Sending request to {model_name}...")
        response = model.generate_content(prompt)
        
        # Clean and return
        cleaned_text = clean_json_text(response.text)
        return cleaned_text

    except Exception as e:
        print(f"❌ AI Processing Error: {e}")
        # Return error JSON to prevent crash
        return json.dumps([
            {
                "Key": "Error", 
                "Value": "Failed to extract data", 
                "Comments": str(e)
            }
        ])