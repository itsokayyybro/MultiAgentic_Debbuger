"""
Main Execution Script

This is the entry point for the Multi-Agentic Debugger.
It demonstrates the complete workflow with example buggy code.

Run this file to see the system in action:
    python main.py

The script will:
1. Load example buggy code (with multiple error types)
2. Run the debugging workflow
3. Display results in a formatted report

You can also enable debug output:
    DEBUG_ORCHESTRATOR=true DEBUG_LLM=true python main.py
"""

from orchestrator import debug_code
from buggy_code import BUGGY_CODE


# ============================================================================
# OUTPUT FORMATTING FUNCTIONS
# ============================================================================

def print_section_header(title: str):
    """Prints a formatted section header."""
    width = 70
    print("\n" + "=" * width)
    print(f" {title}")
    print("=" * width)


def print_code_block(code: str, title: str = "Code"):
    """Prints code in a formatted block."""
    print(f"\n{'─' * 70}")
    print(f"📄 {title}")
    print('─' * 70)
    for i, line in enumerate(code.split('\n'), 1):
        print(f"{i:3d} | {line}")
    print('─' * 70)


def print_errors(errors: list):
    """Prints detected errors in a formatted list."""
    if not errors:
        print("\n✅ No errors detected.")
        return
    
    print(f"\n🔍 Found {len(errors)} error(s):\n")
    
    for idx, error in enumerate(errors, 1):
        # Format line number
        line_info = f"Line {error['line']}" if error['line'] else "Unknown line"
        
        # Print error with emoji based on type
        emoji = {
            "Syntax": "🔴",
            "Runtime": "🟠", 
            "Logical": "🟡"
        }.get(error['type'], "⚪")
        
        print(f"{idx}. {emoji} [{error['type']}] {line_info}")
        print(f"   → {error['description']}\n")


def print_explanation(text: str):
    """Prints the fix explanation in a formatted box."""
    print("\n💡 What was fixed:")
    print("┌" + "─" * 68 + "┐")
    
    # Wrap long lines
    for line in text.split('\n'):
        if len(line) <= 66:
            print(f"│ {line:<66} │")
        else:
            # Simple word wrapping
            words = line.split()
            current_line = ""
            for word in words:
                if len(current_line + word) <= 66:
                    current_line += word + " "
                else:
                    print(f"│ {current_line:<66} │")
                    current_line = word + " "
            if current_line:
                print(f"│ {current_line:<66} │")
    
    print("└" + "─" * 68 + "┘")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main_execution():
    """Main execution function."""
    
    # Print header
    print("\n" + "🤖" * 35)
    print("        MULTI-AGENTIC CODE DEBUGGER")
    print("🤖" * 35)
    
    # Run debugging workflow
    print_section_header("STEP 2: RUNNING DEBUGGING WORKFLOW")
    print("\nInitializing agents...")
    print("• Scanner Agent: Ready")
    print("• Fixer Agent: Ready")
    print("• Validator Agent: Ready\n")
    
    result = debug_code(BUGGY_CODE)
    
    # Display results
    print_section_header("STEP 3: ANALYSIS RESULTS")
    print_errors(result["detected_errors"])
    
    # Display fix results based on status
    if result["status"] == "FIXED":
        print_section_header("STEP 4: FIXED CODE")
        print_code_block(result["final_code"], "Corrected Code")
        
        # Show explanation from last successful attempt
        last_attempt = result["fix_attempts"][-1]
        print_explanation(last_attempt["explanation"])
        
        print_section_header("✅ SUCCESS!")
        print(f"\nCode successfully debugged in {len(result['fix_attempts'])} attempt(s)!")
        print("The fixed code is ready to run.\n")
        
    elif result["status"] == "NO_ERRORS":
        print_section_header("✅ NO ISSUES FOUND")
        print("\nThe code appears to be error-free!")
        print("No changes were made.\n")
        
    else:  # FAILED
        print_section_header("❌ DEBUGGING FAILED")
        print(f"\nCould not fix the code after {len(result['fix_attempts'])} attempt(s).")
        print("\nAttempted fixes:")
        for attempt in result["fix_attempts"]:
            print(f"\n  Attempt {attempt['attempt']}:")
            print(f"  Status: {attempt['validation'].get('status')}")
            print(f"  Feedback: {attempt['validation'].get('feedback')}")
        print("\nManual intervention may be required.\n")
    
    # Summary
    print_section_header("SUMMARY")
    print(f"\n  Status: {result['status']}")
    print(f"  Errors detected: {len(result['detected_errors'])}")
    print(f"  Fix attempts: {len(result['fix_attempts'])}")
    print()


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    try:
        main_execution()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()