"""
Agent Implementations

This module contains the three core agents of the debugging system:
1. Scanner Agent - Detects errors
2. Fixer Agent - Proposes fixes
3. Validator Agent - Validates fixes

Design Pattern:
Each agent is a stateless function that:
- Takes specific inputs
- Calls the LLM with a specialized prompt
- Returns structured output (dict)

The agents don't communicate directly with each other.
All coordination happens through the orchestrator.
"""

import json
from typing import TypedDict, List

from prompts import SCANNER_PROMPT, FIXER_PROMPT, VALIDATOR_PROMPT
from llm_client import safe_llm_json_call


# =============================================================================
# TYPE DEFINITIONS
# =============================================================================

class ErrorReport(TypedDict, total=False):
    """Error detected by scanner."""
    type: str  # "Syntax", "Runtime", or "Logical"
    line: int | None
    description: str


class ScannerResult(TypedDict):
    """Result from scanner agent."""
    errors: List[ErrorReport]


class FixerResult(TypedDict):
    """Result from fixer agent."""
    fixed_code: str
    explanation: str


class ValidatorResult(TypedDict):
    """Result from validator agent."""
    status: str  # "Approved" or "Rejected"
    feedback: str


# ============================================================================
# SCANNER AGENT
# ============================================================================

def scanner_agent(code: str) -> ScannerResult:
    """
    Analyzes code and detects errors without fixing them.
    
    This agent has a single responsibility: identify problems.
    It categorizes errors into three types:
    - Syntax: Code won't parse (missing colons, wrong indentation)
    - Runtime: Code will crash during execution (division by zero, type errors)
    - Logical: Code runs but produces wrong results (off-by-one, wrong algorithm)
    
    Args:
        code: Python code to analyze (as string)
    
    Returns:
        ScannerResult: {"errors": [...]}
        
    Raises:
        ValueError: If code is empty or invalid JSON in response
        RuntimeError: If LLM call fails
    
    Example:
        >>> result = scanner_agent("def foo()\\n    print('hi')")
        >>> print(len(result["errors"]))
        1
    """
    if not code or not code.strip():
        raise ValueError("Code cannot be empty")
    
    # Inject the code into the scanner prompt
    prompt = SCANNER_PROMPT.replace("{{CODE}}", code)
    
    # Call LLM and parse JSON response
    result = safe_llm_json_call(prompt, required_keys=["errors"])
    
    return ScannerResult(errors=result.get("errors", []))


# ============================================================================
# FIXER AGENT
# ============================================================================

def fixer_agent(code: str, errors: List[ErrorReport]) -> FixerResult:
    """
    Proposes fixes for detected errors with minimal code changes.
    
    This agent receives:
    - The original buggy code
    - A list of errors to fix
    
    It returns:
    - Fixed code (complete, executable)
    - Human-readable explanation of changes
    
    Design Principle: MINIMAL CHANGES
    The fixer should be "surgical" - only change what's broken.
    It should NOT:
    - Refactor working code
    - Add comments
    - Improve style
    - Change variable names
    
    Args:
        code: Original Python code with errors
        errors: List of error dicts from scanner_agent
    
    Returns:
        FixerResult: {"fixed_code": str, "explanation": str}
        
    Raises:
        ValueError: If inputs invalid
        RuntimeError: If LLM call fails
    
    Example:
        >>> errors = [{"type": "Syntax", "line": 1, "description": "Missing colon"}]
        >>> result = fixer_agent("def foo()\\n    pass", errors)
        >>> print(":" in result["fixed_code"])
        True
    """
    if not code or not code.strip():
        raise ValueError("Code cannot be empty")
    
    if not errors or not isinstance(errors, list):
        raise ValueError("Errors must be a non-empty list")
    
    # Validate error structure
    for err in errors:
        if not isinstance(err, dict) or "type" not in err or "description" not in err:
            raise ValueError(f"Invalid error structure: {err}")
    
    # Prepare the prompt with code and errors
    errors_json = json.dumps(errors, indent=2)
    
    prompt = (FIXER_PROMPT
              .replace("{{CODE}}", code)
              .replace("{{ERRORS}}", errors_json))
    
    # Call LLM and parse JSON response
    result = safe_llm_json_call(prompt, required_keys=["fixed_code", "explanation"])
    
    return FixerResult(
        fixed_code=result.get("fixed_code", ""),
        explanation=result.get("explanation", "")
    )


# ============================================================================
# VALIDATOR AGENT
# ============================================================================

def validator_agent(original: str, fixed: str, errors: List[ErrorReport]) -> ValidatorResult:
    """
    Validates that proposed fixes are correct and complete.
    
    This agent acts as quality control. It checks:
    1. Were ALL errors from the list fixed?
    2. Were ANY new errors introduced?
    3. Was unrelated code modified?
    4. Are changes minimal and focused?
    
    The validator is STRICT. It should reject fixes that:
    - Leave any original error unfixed
    - Introduce new bugs
    - Make unnecessary changes
    - Over-refactor the code
    
    Args:
        original: Original buggy code
        fixed: Proposed fixed code
        errors: List of errors that should be resolved
    
    Returns:
        ValidatorResult: {"status": "Approved|Rejected", "feedback": str}
        
    Raises:
        ValueError: If inputs invalid
        RuntimeError: If LLM call fails
    
    Example:
        >>> errors = [{"type": "Syntax", "line": 1, "description": "Missing colon"}]
        >>> original = "def foo()\\n    pass"
        >>> fixed = "def foo():\\n    pass"
        >>> result = validator_agent(original, fixed, errors)
        >>> print(result["status"])
        'Approved'
    """
    if not original or not original.strip():
        raise ValueError("Original code cannot be empty")
    
    if not fixed or not fixed.strip():
        raise ValueError("Fixed code cannot be empty")
    
    if not errors or not isinstance(errors, list):
        raise ValueError("Errors must be a non-empty list")
    
    # Prepare the prompt with all context
    errors_json = json.dumps(errors, indent=2)
    
    prompt = (VALIDATOR_PROMPT
              .replace("{{ORIGINAL}}", original)
              .replace("{{FIXED}}", fixed)
              .replace("{{ERRORS}}", errors_json))
    
    # Call LLM and parse JSON response
    result = safe_llm_json_call(prompt, required_keys=["status", "feedback"])
    
    return ValidatorResult(
        status=result.get("status", "Rejected"),
        feedback=result.get("feedback", "No feedback provided")
    )


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def format_errors_for_display(errors: list) -> str:
    """
    Formats error list for human-readable display.
    
    Args:
        errors: List of error dicts
    
    Returns:
        Formatted string for printing
    """
    if not errors:
        return "No errors detected ✅"
    
    lines = []
    for i, err in enumerate(errors, 1):
        line_info = f"Line {err['line']}" if err['line'] else "Line unknown"
        lines.append(f"{i}. [{err['type']}] {line_info}")
        lines.append(f"   → {err['description']}")
    
    return "\n".join(lines)


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    # Quick test of agents
    print("Testing Scanner Agent...")
    
    test_code = """
def calculate_average(numbers)
    return sum(numbers) / len(numbers)
"""
    
    result = scanner_agent(test_code)
    print(f"Found {len(result['errors'])} errors:")
    print(format_errors_for_display(result['errors']))