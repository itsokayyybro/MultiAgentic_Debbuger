"""
Orchestrator Module

The orchestrator coordinates all agents and manages the debugging workflow.
It implements the multi-agent system's control flow and maintains shared state.

Workflow:
1. Scanner detects errors
2. If errors found → Fixer proposes solution
3. Validator reviews the fix
4. If rejected → Retry (up to MAX_FIX_RETRIES)
5. If approved → Return fixed code

Key Responsibilities:
- Agent coordination (who runs when)
- State management (shared context between agents)
- Retry logic (handling validation failures)
- Result aggregation (collecting all attempts)
"""

import textwrap
from typing import Dict, Any, List

from agents import scanner_agent, fixer_agent, validator_agent
from config import MAX_FIX_RETRIES, DEBUG_ORCHESTRATOR


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def normalize_code(code: str) -> str:
    """
    Normalizes code formatting for consistent output.
    
    Problems this solves:
    - LLMs sometimes add extra indentation
    - Inconsistent leading/trailing whitespace
    - Mixed indentation styles
    
    Actions:
    1. Removes common leading indentation (dedent)
    2. Strips leading/trailing whitespace
    
    Args:
        code: Python code string
    
    Returns:
        Normalized code string
    
    Example:
        >>> code = "    def foo():\\n        pass\\n"
        >>> print(normalize_code(code))
        'def foo():\\n    pass'
    """
    return textwrap.dedent(code).strip()


# ============================================================================
# MAIN ORCHESTRATOR FUNCTION
# ============================================================================

def debug_code(code: str) -> Dict[str, Any]:
    """
    Main orchestration function that runs the complete debugging workflow.
    
    This is the primary entry point for the debugging system. It:
    1. Initializes shared state
    2. Runs Scanner to detect errors
    3. Runs Fixer to propose solutions (if errors found)
    4. Runs Validator to check fixes
    5. Implements retry logic
    6. Returns comprehensive results
    
    State Management:
    The function maintains a 'state' dict that serves as shared memory
    between agent calls. This allows us to:
    - Track all fix attempts
    - Preserve original code
    - Store detected errors
    - Record validation results
    
    Args:
        code: Python code string to debug
    
    Returns:
        dict: {
            "original_code": str,           # Input code
            "detected_errors": list,        # Errors found by scanner
            "fix_attempts": list,           # All fix attempts (may be multiple)
            "final_code": str or None,      # Final fixed code (if successful)
            "status": str                   # "FIXED" | "NO_ERRORS" | "FAILED"
        }
    
    Status Values:
    - "NO_ERRORS": Scanner found no issues
    - "FIXED": Code successfully debugged
    - "FAILED": Could not fix after MAX_FIX_RETRIES attempts
    - "IN_PROGRESS": Temporary status during execution
    
    Example:
        >>> buggy = "def foo()\\n    pass"
        >>> result = debug_code(buggy)
        >>> print(result["status"])
        'FIXED'
        >>> print(result["final_code"])
        'def foo():\\n    pass'
    """
    
    # ========================================================================
    # STEP 1: Initialize shared state
    # ========================================================================
    # This state dict is passed through the entire workflow
    # and accumulates information from each agent
    
    state: Dict[str, Any] = {
        "original_code": code,       # Preserve input for reference
        "detected_errors": [],       # Will be filled by scanner
        "fix_attempts": [],          # List of all fix attempts
        "final_code": None,          # Set when fix is approved
        "status": "IN_PROGRESS"      # Current workflow status
    }
    
    # ========================================================================
    # STEP 2: Run Scanner Agent
    # ========================================================================
    # Scanner analyzes the code and detects all errors
    # It returns a list of error objects
    
    if DEBUG_ORCHESTRATOR:
        print(f"🔧 [DEBUG] Starting debugging workflow")
    
    print("🔍 Scanning code for errors...")
    
    try:
        scan_result = scanner_agent(code)
        state["detected_errors"] = scan_result.get("errors", [])
    except Exception as e:
        print(f"❌ Scanner failed: {e}")
        state["status"] = "FAILED"
        return state
    
    # If no errors found, we're done!
    if not state["detected_errors"]:
        print("✅ No errors detected!")
        state["status"] = "NO_ERRORS"
        state["final_code"] = code
        return state
    
    print(f"Found {len(state['detected_errors'])} error(s)")
    
    # ========================================================================
    # STEP 3: Fix-Validate Loop with Retry Logic
    # ========================================================================
    # Try to fix the code up to MAX_FIX_RETRIES times
    # Each iteration:
    # 1. Fixer proposes a solution
    # 2. Validator checks the solution
    # 3. If approved → Success! Exit loop
    # 4. If rejected → Try again (or fail if out of retries)
    
    for attempt_num in range(MAX_FIX_RETRIES):
        print(f"\n🔧 Fix attempt {attempt_num + 1}/{MAX_FIX_RETRIES}...")
        
        try:
            # -------- STEP 3A: Fixer proposes a solution --------
            fix_result = fixer_agent(code, state["detected_errors"])
            
            if DEBUG_ORCHESTRATOR:
                print(f"🔧 [DEBUG] Fix proposed, length: {len(fix_result.get('fixed_code', ''))}")
            
            print(f"✏️  Proposed fix generated")
            
            # -------- STEP 3B: Validator reviews the fix --------
            validation_result = validator_agent(
                state["original_code"],
                fix_result["fixed_code"],
                state["detected_errors"]
            )
            
            if DEBUG_ORCHESTRATOR:
                print(f"🔧 [DEBUG] Validation status: {validation_result.get('status')}")
            
            print(f"🔎 Validation: {validation_result['status']}")
            
            # -------- Record this attempt in state --------
            state["fix_attempts"].append({
                "attempt": attempt_num + 1,
                "fixed_code": fix_result["fixed_code"],
                "explanation": fix_result["explanation"],
                "validation": validation_result
            })
            
            # -------- STEP 3C: Check validation result --------
            if validation_result.get("status", "").lower() == "approved":
                # Success! Fix is approved
                print("✅ Fix approved!")
                state["final_code"] = normalize_code(fix_result["fixed_code"])
                state["status"] = "FIXED"
                return state
            else:
                # Fix rejected, will retry if attempts remain
                feedback = validation_result.get("feedback", "Unknown reason")
                print(f"❌ Fix rejected: {feedback}")
                
        except Exception as e:
            print(f"❌ Error during fix attempt {attempt_num + 1}: {e}")
            if DEBUG_ORCHESTRATOR:
                import traceback
                traceback.print_exc()
            continue
    
    # ========================================================================
    # STEP 4: All retry attempts exhausted
    # ========================================================================
    # If we get here, we couldn't fix the code after MAX_FIX_RETRIES attempts
    print(f"\n❌ Failed to fix code after {MAX_FIX_RETRIES} attempts")
    state["status"] = "FAILED"
    return state


# ============================================================================
# ADDITIONAL UTILITY FUNCTIONS
# ============================================================================

def get_summary(result: dict) -> str:
    """
    Generates a human-readable summary of debugging results.
    
    Args:
        result: Output from debug_code()
    
    Returns:
        Multi-line string summary
    """
    lines = []
    lines.append(f"Status: {result['status']}")
    lines.append(f"Errors detected: {len(result['detected_errors'])}")
    lines.append(f"Fix attempts: {len(result['fix_attempts'])}")
    
    if result['status'] == 'FIXED':
        lines.append("✅ Successfully debugged!")
    elif result['status'] == 'NO_ERRORS':
        lines.append("✅ No errors found!")
    else:
        lines.append("❌ Could not fix automatically")
    
    return "\n".join(lines)


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    # Quick test of orchestrator
    test_code = """
def calculate_average(numbers)
    return sum(numbers) / len(numbers)
"""
    
    print("Testing Orchestrator...")
    print("=" * 50)
    
    result = debug_code(test_code)
    
    print("\n" + "=" * 50)
    print("RESULTS:")
    print(get_summary(result))
    
    if result['status'] == 'FIXED':
        print("\nFixed code:")
        print(result['final_code'])