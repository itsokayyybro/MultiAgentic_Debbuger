import os
import json
import re

USE_GEMINI = False  # 🔁 Set True ONLY for final demo

if USE_GEMINI:
    import google.generativeai as genai
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

    model = genai.GenerativeModel(
        "models/gemini-2.5-flash",
        generation_config={"temperature": 0.2}
    )


def mock_llm(prompt: str) -> str:
    if "Scanner Agent" in prompt:
        return """
        {
          "errors": [
            {
              "type": "Syntax",
              "line": 1,
              "description": "Unclosed string literal"
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
          "feedback": "Fix resolves the syntax error"
        }
        """

    return "{}"


def call_llm(prompt: str) -> str:
    if USE_GEMINI:
        response = model.generate_content(prompt)
        return response.text.strip()
    return mock_llm(prompt)


def extract_json(text: str) -> dict:
    text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE).strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON detected in LLM output")
    return json.loads(match.group(0))


def safe_llm_json_call(prompt: str) -> dict:
    raw = call_llm(prompt)
    return extract_json(raw)
