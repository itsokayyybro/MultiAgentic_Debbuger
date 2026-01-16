"""
Configuration Module

Supports multiple LLM providers (Gemini, Ollama, Mock)
"""

import os

# =============================================================================
# LLM PROVIDER SELECTION
# =============================================================================

# LLM_PROVIDER can be: "gemini", "ollama", "mock"
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "").strip().lower()

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")

# Ollama defaults (local)
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434").strip()
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.1:8b").strip()
OLLAMA_TIMEOUT = float(os.environ.get("OLLAMA_TIMEOUT", "60"))

# If provider not set, auto-pick based on available config
if not LLM_PROVIDER:
    if GOOGLE_API_KEY:
        LLM_PROVIDER = "gemini"
    elif OLLAMA_MODEL or OLLAMA_HOST:
        LLM_PROVIDER = "ollama"
    else:
        LLM_PROVIDER = "mock"

USE_GOOGLE_AI = LLM_PROVIDER == "gemini" and bool(GOOGLE_API_KEY)

# =============================================================================
# MODEL CONFIGURATION
# =============================================================================

# Primary model to use (recommended: gemini-flash-latest)
GEMINI_MODEL = "gemini-flash-latest"

# Fallback models (tried in order if primary fails)
FALLBACK_MODELS = [
    "gemini-pro-latest",
    "gemini-2.5-flash-lite",
    "gemini-3-flash-preview",
    "gemini-2.0-flash-lite-preview",
]

# All available models on your account (for reference)
AVAILABLE_MODELS = [
    "gemini-flash-latest",           # ✅ Recommended - Fast and capable
    "gemini-pro-latest",              # ✅ More capable, slower
    "gemini-flash-lite-latest",      # Fast, less capable
    "gemini-2.5-flash-lite",         # Lightweight
    "gemini-3-flash-preview",        # Preview of Gemini 3
    "gemini-3-pro-preview",          # Most capable, slower
    "gemini-2.0-flash-lite-preview",
    "gemini-exp-1206",
    # ... and many more (see full list in your output)
]

# =============================================================================
# LLM GENERATION PARAMETERS
# =============================================================================

TEMPERATURE = 0.2  # Lower = more deterministic (0.0-1.0)
MAX_OUTPUT_TOKENS = 8000  # Maximum response length

# =============================================================================
# RETRY CONFIGURATION
# =============================================================================

MAX_API_RETRIES = 2  # Number of retries for transient errors
INITIAL_RETRY_DELAY = 2.0  # seconds
RETRY_BACKOFF_MULTIPLIER = 2.0  # Exponential backoff (2s, 4s, 8s...)

# =============================================================================
# ORCHESTRATOR CONFIGURATION
# =============================================================================

MAX_FIX_RETRIES = 3  # How many times to attempt fixing code

# =============================================================================
# DEBUG FLAGS
# =============================================================================

DEBUG_LLM = os.environ.get("DEBUG_LLM", "false").lower() == "true"
DEBUG_ORCHESTRATOR = os.environ.get("DEBUG_ORCHESTRATOR", "false").lower() == "true"

# =============================================================================
# VALIDATION
# =============================================================================

if LLM_PROVIDER == "gemini" and not GOOGLE_API_KEY:
    print("⚠️  LLM_PROVIDER=gemini but GOOGLE_API_KEY is not set")
    print("   Set it with: export GOOGLE_API_KEY='your-key-here'")

# =============================================================================
# INFO
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("CONFIGURATION")
    print("=" * 70)
    print(f"LLM Provider: {LLM_PROVIDER}")
    print(f"API Key Set: {bool(GOOGLE_API_KEY)}")
    print(f"Use Google AI: {USE_GOOGLE_AI}")
    print(f"Ollama Host: {OLLAMA_HOST}")
    print(f"Ollama Model: {OLLAMA_MODEL}")
    print(f"Primary Model: {GEMINI_MODEL}")
    print(f"Fallback Models: {', '.join(FALLBACK_MODELS[:2])}...")
    print(f"Max Fix Retries: {MAX_FIX_RETRIES}")
    print(f"Temperature: {TEMPERATURE}")
    print(f"Debug Mode: LLM={DEBUG_LLM}, Orchestrator={DEBUG_ORCHESTRATOR}")
    print("=" * 70)
    print()
    print("Available models on your account:")
    for model in AVAILABLE_MODELS[:10]:
        print(f"  • {model}")
    print(f"  ... and {len(AVAILABLE_MODELS) - 10} more")
    print("=" * 70)