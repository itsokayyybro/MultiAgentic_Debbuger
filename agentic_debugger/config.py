"""
Configuration Module

Using google.generativeai with available models
"""

import os

# =============================================================================
# GOOGLE AI (Gemini) CONFIGURATION
# =============================================================================

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
USE_GOOGLE_AI = bool(GOOGLE_API_KEY)

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

if USE_GOOGLE_AI and not GOOGLE_API_KEY:
    print("⚠️  USE_GOOGLE_AI is True but GOOGLE_API_KEY is not set")
    print("   Set it with: export GOOGLE_API_KEY='your-key-here'")

# =============================================================================
# INFO
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("CONFIGURATION")
    print("=" * 70)
    print(f"API Key Set: {bool(GOOGLE_API_KEY)}")
    print(f"Use Google AI: {USE_GOOGLE_AI}")
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