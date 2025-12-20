import json
from prompts import SCANNER_PROMPT, FIXER_PROMPT, VALIDATOR_PROMPT
from llm_client import safe_llm_json_call

def scanner_agent(code):
    prompt = SCANNER_PROMPT.replace("{{CODE}}", code)
    return safe_llm_json_call(prompt)

def fixer_agent(code, errors):
    prompt = FIXER_PROMPT \
        .replace("{{CODE}}", code) \
        .replace("{{ERRORS}}", json.dumps(errors, indent=2))
    return safe_llm_json_call(prompt)

def validator_agent(original, fixed, errors):
    prompt = VALIDATOR_PROMPT \
        .replace("{{ORIGINAL}}", original) \
        .replace("{{FIXED}}", fixed) \
        .replace("{{ERRORS}}", json.dumps(errors, indent=2))
    return safe_llm_json_call(prompt)
