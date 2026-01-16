"""
LLM Client Module

Supports Gemini (google.generativeai) and Ollama (local) with fallback.
"""

import json
import os
import re
import time
import urllib.request
from typing import Dict, Any, Optional

from config import (
    LLM_PROVIDER,
    USE_GOOGLE_AI,
    GOOGLE_API_KEY,
    GEMINI_MODEL,
    FALLBACK_MODELS,
    TEMPERATURE,
    MAX_OUTPUT_TOKENS,
    DEBUG_LLM,
    MAX_API_RETRIES,
    INITIAL_RETRY_DELAY,
    RETRY_BACKOFF_MULTIPLIER,
    OLLAMA_HOST,
    OLLAMA_MODEL,
    OLLAMA_TIMEOUT,
)

# =============================================================================
# STATE
# =============================================================================

current_model = None
model_instance = None
_GEMINI_INITIALIZED = False
_current_provider = LLM_PROVIDER
_current_model_name = (
    GEMINI_MODEL if LLM_PROVIDER == "gemini" else
    OLLAMA_MODEL if LLM_PROVIDER == "ollama" else
    "mock"
)

# =============================================================================
# INITIALIZE GEMINI
# =============================================================================

def initialize_gemini() -> bool:
    """Initializes Gemini client if possible."""
    global model_instance, _GEMINI_INITIALIZED, _current_model_name

    if not GOOGLE_API_KEY:
        _GEMINI_INITIALIZED = False
        return False

    try:
        import google.generativeai as genai

        genai.configure(api_key=GOOGLE_API_KEY)

        model_instance = genai.GenerativeModel(
            GEMINI_MODEL,
            generation_config={
                "temperature": TEMPERATURE,
                "max_output_tokens": MAX_OUTPUT_TOKENS,
            }
        )

        _GEMINI_INITIALIZED = True
        _current_model_name = GEMINI_MODEL
        if DEBUG_LLM:
            print(f"✅ Gemini initialized: {GEMINI_MODEL}")
        return True

    except ImportError:
        print("❌ google-generativeai not installed")
        print("   Install: pip install google-generativeai")
        _GEMINI_INITIALIZED = False
        return False

    except Exception as e:
        print(f"⚠️  Primary model '{GEMINI_MODEL}' init failed: {e}")
        print("   Will try fallback models on first call")
        _GEMINI_INITIALIZED = False
        return False


if USE_GOOGLE_AI and GOOGLE_API_KEY:
    initialize_gemini()

# =============================================================================
# MOCK LLM
# =============================================================================

def mock_llm(prompt: str) -> str:
    """Mock responses for testing without API."""
    if "Scanner" in prompt:
        return json.dumps({
            "errors": [{
                "type": "Syntax",
                "line": 1,
                "description": "Missing colon after function definition"
            }]
        })
    
    if "Fixer" in prompt:
        return json.dumps({
            "fixed_code": 'def foo():\n    pass',
            "explanation": "Added missing colon after function definition"
        })
    
    if "Validator" in prompt:
        return json.dumps({
            "status": "Approved",
            "feedback": "The fix correctly resolves the syntax error"
        })
    
    return "{}"

# =============================================================================
# OLLAMA CLIENT
# =============================================================================

def call_ollama(prompt: str) -> str:
    """Calls local Ollama server and returns response text."""
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": TEMPERATURE,
        },
    }

    if MAX_OUTPUT_TOKENS:
        payload["options"]["num_predict"] = MAX_OUTPUT_TOKENS

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{OLLAMA_HOST.rstrip('/')}/api/generate",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT) as response:
        body = response.read().decode("utf-8")
        result = json.loads(body)
        return result.get("response", "").strip()

# =============================================================================
# MODEL FALLBACK
# =============================================================================

def try_fallback_models() -> bool:
    """
    Tries to initialize a fallback model if primary failed.
    
    Returns:
        bool: True if a fallback model worked
    """
    global model_instance, _GEMINI_INITIALIZED, _current_model_name
    
    if not GOOGLE_API_KEY:
        return False
    
    try:
        import google.generativeai as genai
        
        for fallback_model in FALLBACK_MODELS:
            try:
                print(f"🔄 Trying fallback model: {fallback_model}...")
                
                model_instance = genai.GenerativeModel(
                    fallback_model,
                    generation_config={
                        "temperature": TEMPERATURE,
                        "max_output_tokens": MAX_OUTPUT_TOKENS,
                    }
                )
                
                # Test it with a simple call
                test_response = model_instance.generate_content("Say 'ok'")
                
                _GEMINI_INITIALIZED = True
                _current_model_name = fallback_model
                print(f"✅ Fallback successful! Using: {fallback_model}")
                return True
                
            except Exception as e:
                if DEBUG_LLM:
                    print(f"   ❌ {fallback_model} failed: {str(e)[:50]}...")
                continue
        
        print("❌ All fallback models failed")
        return False
        
    except Exception as e:
        print(f"❌ Fallback attempt failed: {e}")
        return False

# =============================================================================
# ERROR CLASSIFICATION
# =============================================================================

def classify_error(error: Exception) -> str:
    """Classifies error into categories."""
    error_msg = str(error).lower()
    
    # Quota/Rate limit
    if any(x in error_msg for x in ["resource_exhausted", "quota", "429", "rate limit"]):
        return "quota"
    
    # Authentication
    if any(x in error_msg for x in ["authentication", "api key", "unauthenticated", "invalid key"]):
        return "auth"
    
    # Permission
    if any(x in error_msg for x in ["permission", "forbidden", "403"]):
        return "auth"
    
    # Model not found
    if any(x in error_msg for x in ["not found", "404", "unknown model"]):
        return "model"
    
    # Network issues
    if any(x in error_msg for x in ["connection", "timeout", "network"]):
        return "network"
    
    # Server errors
    if any(x in error_msg for x in ["500", "503", "internal", "server error"]):
        return "server"
    
    return "unknown"

# =============================================================================
# LLM CALL WITH AUTOMATIC FALLBACK
# =============================================================================

def call_gemini(prompt: str) -> str:
    """Calls Gemini with automatic model fallback and error handling."""
    global model_instance, _GEMINI_INITIALIZED, _current_model_name

    if not _GEMINI_INITIALIZED:
        if GOOGLE_API_KEY:
            if DEBUG_LLM:
                print("🔄 Gemini not initialized, trying fallbacks...")
            if not try_fallback_models():
                if DEBUG_LLM:
                    print("ℹ️  Using mock mode (no models available)")
                return mock_llm(prompt)
        else:
            if DEBUG_LLM:
                print("ℹ️  Using mock mode (no API key)")
            return mock_llm(prompt)

    retry_delay = INITIAL_RETRY_DELAY
    last_error = None

    for attempt in range(MAX_API_RETRIES + 1):
        try:
            if DEBUG_LLM:
                print(f"📤 Calling {_current_model_name} (attempt {attempt + 1})...")

            response = model_instance.generate_content(prompt)

            if DEBUG_LLM:
                print(f"✅ Response received ({len(response.text)} chars)")

            return response.text.strip()

        except Exception as e:
            last_error = e
            error_category = classify_error(e)

            if DEBUG_LLM:
                print(f"⚠️  Error: {type(e).__name__} ({error_category})")
                print(f"    Message: {str(e)[:100]}")

            if error_category == "model":
                print(f"❌ Model '{_current_model_name}' not available")
                if try_fallback_models():
                    continue
                print("⚠️  All models failed, falling back to mock mode\n")
                return mock_llm(prompt)

            if error_category == "auth":
                print("\n" + "=" * 70)
                print("❌ AUTHENTICATION ERROR")
                print("=" * 70)
                print("Your API key is invalid or lacks permissions.")
                print()
                print("Solutions:")
                print("1. Get new key: https://aistudio.google.com/app/apikey")
                print("2. Set it: export GOOGLE_API_KEY='your-key-here'")
                print("3. Verify: echo $GOOGLE_API_KEY")
                print("=" * 70)
                print("\n⚠️  Falling back to mock mode\n")
                return mock_llm(prompt)

            if error_category == "quota":
                print("\n" + "=" * 70)
                print("❌ QUOTA EXHAUSTED")
                print("=" * 70)
                print("You've hit your API rate/quota limits.")
                print()
                print("Free tier limits:")
                print("  • 15 requests per minute")
                print("  • 1,500 requests per day")
                print()
                print("Solutions:")
                print("  1. Wait 60 seconds (rate limit resets)")
                print("  2. Wait until tomorrow (daily quota resets)")
                print("  3. Check usage: https://aistudio.google.com")
                print("=" * 70)
                print("\n⚠️  Falling back to mock mode\n")
                return mock_llm(prompt)

            if error_category in ["network", "server"]:
                if attempt < MAX_API_RETRIES:
                    print(f"⚠️  {error_category.upper()} error, retrying in {retry_delay}s...")
                    time.sleep(retry_delay)
                    retry_delay *= RETRY_BACKOFF_MULTIPLIER
                    continue
                print(f"❌ {error_category.upper()} error after {MAX_API_RETRIES} retries")
                print("⚠️  Falling back to mock mode\n")
                return mock_llm(prompt)

            print(f"\n❌ Unexpected error: {type(e).__name__}")
            print(f"   {str(e)[:150]}")
            print("⚠️  Falling back to mock mode\n")
            return mock_llm(prompt)

    if last_error:
        print(f"❌ All retries exhausted: {last_error}")
    return mock_llm(prompt)


def call_llm(prompt: str) -> str:
    """
    Routes calls to the selected LLM provider with fallback.

    Returns:
        str: LLM response
    """
    global _current_provider, _current_model_name

    if LLM_PROVIDER == "ollama":
        try:
            if DEBUG_LLM:
                print(f"📤 Calling Ollama ({OLLAMA_MODEL})...")
            _current_provider = "ollama"
            _current_model_name = OLLAMA_MODEL
            return call_ollama(prompt)
        except Exception as e:
            if DEBUG_LLM:
                print(f"⚠️  Ollama error: {type(e).__name__} - {str(e)[:120]}")
            if GOOGLE_API_KEY:
                if DEBUG_LLM:
                    print("🔁 Falling back to Gemini")
                initialize_gemini()
                _current_provider = "gemini"
                return call_gemini(prompt)
            if DEBUG_LLM:
                print("ℹ️  Falling back to mock mode")
            return mock_llm(prompt)

    if LLM_PROVIDER == "gemini":
        _current_provider = "gemini"
        if not _GEMINI_INITIALIZED:
            initialize_gemini()
        return call_gemini(prompt)

    _current_provider = "mock"
    return mock_llm(prompt)

# =============================================================================
# JSON EXTRACTION
# =============================================================================

def extract_json(text: str) -> str:
    """Extracts JSON object from text."""
    # Remove markdown code blocks
    text = re.sub(r"```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```\s*$", "", text, flags=re.IGNORECASE | re.MULTILINE)
    
    # Find balanced JSON object
    stack = []
    start = None
    in_string = False
    escape_next = False
    
    for i, ch in enumerate(text):
        if escape_next:
            escape_next = False
            continue
        
        if ch == "\\" and in_string:
            escape_next = True
            continue
        
        if ch == '"' and not escape_next:
            in_string = not in_string
            continue
        
        if in_string:
            continue
        
        if ch == "{":
            if not stack:
                start = i
            stack.append(ch)
        elif ch == "}":
            if stack:
                stack.pop()
                if not stack and start is not None:
                    json_str = text[start:i + 1]
                    try:
                        json.loads(json_str)  # Validate
                        return json_str
                    except json.JSONDecodeError:
                        continue
    
    raise ValueError(f"No valid JSON in response: {text[:200]}...")

def safe_llm_json_call(prompt: str, required_keys: Optional[list] = None) -> Dict[str, Any]:
    """
    Safely calls LLM and extracts/validates JSON.
    
    Args:
        prompt: The prompt to send
        required_keys: Optional list of required keys
    
    Returns:
        dict: Parsed JSON response
    """
    raw = call_llm(prompt)
    
    if DEBUG_LLM:
        print("\n" + "-" * 60)
        print("RAW OUTPUT:")
        print(raw[:500] + ("..." if len(raw) > 500 else ""))
        print("-" * 60 + "\n")
    
    json_str = extract_json(raw)
    parsed = json.loads(json_str)
    
    # Validate required keys
    if required_keys:
        missing = [k for k in required_keys if k not in parsed]
        if missing:
            raise ValueError(f"Missing required keys: {missing}")
    
    return parsed

# =============================================================================
# TEST
# =============================================================================

def test_connection():
    """Tests LLM connection."""
    print("\n" + "=" * 70)
    print("🧪 TESTING LLM CONNECTION")
    print("=" * 70 + "\n")
    
    try:
        result = safe_llm_json_call(
            'Return this exact JSON: {"message": "Hello", "status": "working"}',
            required_keys=["message", "status"]
        )
        print("✅ Connection test PASSED!")
        print(f"   Model: {_current_model_name}")
        print(f"   Response: {result}\n")
        return True
        
    except Exception as e:
        print(f"❌ Connection test FAILED: {e}\n")
        return False

# =============================================================================
# INFO
# =============================================================================

def get_current_model() -> str:
    """Returns the currently active model name."""
    return _current_model_name


def get_current_provider() -> str:
    """Returns the currently active provider."""
    return _current_provider

if __name__ == "__main__":
    print(f"Provider: {_current_provider}")
    print(f"Gemini Initialized: {_GEMINI_INITIALIZED}")
    print(f"Current Model: {_current_model_name}")
    test_connection()