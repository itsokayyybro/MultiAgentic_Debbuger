import json
import os
import re

USE_GEMINI = True  # 🔁 Turn TRUE only for final demo

if USE_GEMINI:
    import google.generativeai as genai
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    model = genai.GenerativeModel(
        "models/gemini-2.5-flash",
        generation_config={"temperature": 0.2}
    )

def mock_llm(prompt: str) -> str:
    if "Scanner agent" in prompt:
        return """
        {
          "errors": [
            {
              "type": "Syntax",
              "line": 1,
              "description": "Missing closing quote in print statement"
            }
          ]
        }
        """

    if "Fixer Agent" in prompt:
        return """
        {
          "fixed_code": "print(\\"Hello\\")",
          "explanation": "Added missing closing quote"
        }
        """

    if "Validator Agent" in prompt:
        return """
        {
          "status": "Approved",
          "feedback": "Fix resolves the syntax issue"
        }
        """

    return "{}"

def call_llm(prompt: str) -> str:
    if USE_GEMINI:
        response = model.generate_content(prompt)
        return response.text.strip()
    else:
        return mock_llm(prompt)

def extract_json(text: str) -> str:
    text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE).strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found")
    return match.group(0)

DEBUG_LLM = False  # 🔁 Set True only while debugging

def safe_llm_json_call(prompt: str) -> dict:
    raw = call_llm(prompt)

    if DEBUG_LLM:
        print("\n--- RAW LLM OUTPUT ---")
        print(raw)
        print("----------------------\n")

    return json.loads(extract_json(raw))
