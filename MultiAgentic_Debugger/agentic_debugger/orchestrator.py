from agentic_debugger.agents import (
    scanner_agent,
    fixer_agent,
    validator_agent
)

MAX_FIX_ATTEMPTS = 2


def debug_code(code: str) -> dict:
    """
    Orchestrates the multi-agent debugging process.
    Scanner → Fixer → Validator
    """

    state = {
        "original_code": code,
        "detected_errors": [],
        "fix_attempts": [],
        "final_code": None,
        "status": "IN_PROGRESS"
    }

    # ---------------- SCANNER ----------------
    scan_result = scanner_agent(code)
    state["detected_errors"] = scan_result.get("errors", [])

    # If no errors, exit early
    if not state["detected_errors"]:
        state["status"] = "NO_ERRORS"
        state["final_code"] = code
        return state

    # ---------------- FIX + VALIDATE LOOP ----------------
    for attempt in range(MAX_FIX_ATTEMPTS):

        fix_result = fixer_agent(
            code=state["original_code"],
            errors=state["detected_errors"]
        )

        validation_result = validator_agent(
            original=state["original_code"],
            fixed=fix_result["fixed_code"],
            errors=state["detected_errors"]
        )

        state["fix_attempts"].append({
            "attempt": attempt + 1,
            "fixed_code": fix_result["fixed_code"],
            "explanation": fix_result["explanation"],
            "validation": validation_result
        })

        # Validator has final authority
        if validation_result["status"] == "Approved":
            state["final_code"] = fix_result["fixed_code"]
            state["status"] = "FIXED"
            return state

    # ---------------- FAILURE ----------------
    state["status"] = "FAILED"
    return state
