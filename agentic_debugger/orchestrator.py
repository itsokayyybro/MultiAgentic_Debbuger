from agents import scanner_agent, fixer_agent, validator_agent
import textwrap

MAX_RETRIES = 2

def normalize_code(code: str) -> str:
    """
    Cleans indentation and whitespace
    """
    return textwrap.dedent(code).strip()

def debug_code(code):
    state = {
        "original_code": code,
        "detected_errors": [],
        "fix_attempts": [],
        "final_code": None,
        "status": "IN_PROGRESS"
    }

    scan = scanner_agent(code)
    state["detected_errors"] = scan["errors"]

    if not state["detected_errors"]:
        state["status"] = "NO_ERRORS"
        state["final_code"] = code
        return state

    for attempt in range(MAX_RETRIES):
        fix = fixer_agent(code, state["detected_errors"])

        validation = validator_agent(
            state["original_code"],
            fix["fixed_code"],
            state["detected_errors"]
        )

        state["fix_attempts"].append({
            "attempt": attempt + 1,
            "fixed_code": fix["fixed_code"],
            "explanation": fix["explanation"],
            "validation": validation
        })

        if validation["status"] == "Approved":
            state["final_code"] = normalize_code(fix["fixed_code"])
            state["status"] = "FIXED"
            return state

    state["status"] = "FAILED"
    return state
