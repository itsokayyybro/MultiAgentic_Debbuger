"""
Quick Model Test

Tests the recommended models from your available list.

Usage:
    python test_models.py
"""

import os
import sys

print("\n" + "=" * 70)
print("🧪 TESTING YOUR AVAILABLE MODELS")
print("=" * 70 + "\n")

# Check API key
api_key = os.environ.get("GOOGLE_API_KEY", "")
if not api_key:
    print("❌ GOOGLE_API_KEY not set!")
    sys.exit(1)

print(f"✅ API key found")
print()

# Import SDK
try:
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    print("✅ google-generativeai configured")
except Exception as e:
    print(f"❌ Failed: {e}")
    sys.exit(1)

print()
print("Testing recommended models...")
print("-" * 70)

# Test your available models
models_to_test = [
    ("gemini-flash-latest", "✨ Recommended - Fast and capable"),
    ("gemini-pro-latest", "🚀 More capable, slightly slower"),
    ("gemini-2.5-flash-lite", "⚡ Lightweight option"),
    ("gemini-3-flash-preview", "🔬 Preview of Gemini 3"),
]

working = []
failed = []

for model_name, description in models_to_test:
    try:
        print(f"\n{description}")
        print(f"Testing: {model_name}...")
        
        model = genai.GenerativeModel(
            model_name,
            generation_config={
                "temperature": 0.2,
                "max_output_tokens": 100,
            }
        )
        
        response = model.generate_content("Return JSON: {\"test\": \"success\"}")
        text = response.text
        
        print(f"  ✅ SUCCESS!")
        print(f"  Response: {text[:80]}...")
        working.append(model_name)
        
    except Exception as e:
        error = str(e)
        print(f"  ❌ FAILED")
        
        if "quota" in error.lower() or "429" in error:
            print(f"  Reason: QUOTA EXHAUSTED (wait 60s)")
            failed.append((model_name, "quota"))
        elif "404" in error or "not found" in error.lower():
            print(f"  Reason: MODEL NOT FOUND")
            failed.append((model_name, "not_found"))
        else:
            print(f"  Reason: {error[:80]}...")
            failed.append((model_name, "other"))

# Summary
print("\n" + "=" * 70)
print("📊 RESULTS")
print("=" * 70 + "\n")

if working:
    print(f"✅ {len(working)} model(s) working:")
    for m in working:
        print(f"   • {m}")
    print()
    print(f"✨ RECOMMENDED: config.py is already set to use: {working[0]}")
    print()
else:
    print("❌ No models are currently working")
    print()
    
    # Check if all quota errors
    quota_errors = [m for m, reason in failed if reason == "quota"]
    if len(quota_errors) == len(failed):
        print("🕐 ALL MODELS HAVE QUOTA ERRORS!")
        print()
        print("Your API quota is temporarily exhausted.")
        print()
        print("Quick fixes:")
        print("  1. Wait 60 seconds and run this test again")
        print("  2. Check your quota: https://aistudio.google.com")
        print()
        print("Meanwhile, you can:")
        print("  • Edit config.py: USE_GOOGLE_AI = False")
        print("  • Run: python main.py")
        print("  • The system will use MOCK MODE (no API calls)")
        print()

if failed and working:
    print(f"⚠️  {len(failed)} model(s) failed (but others work):")
    for m, reason in failed:
        print(f"   • {m}: {reason.upper()}")
    print()

print("=" * 70)
print()

if working:
    print("🎉 You're all set! Run: python main.py")
else:
    print("⏰ Wait for quota reset, then run: python main.py")