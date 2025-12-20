from orchestrator import debug_code

def print_code_block(title, code):
    print(f"\n{'=' * 10} {title} {'=' * 10}")
    print(code)
    print("=" * (22 + len(title)))

def print_errors(errors):
    if not errors:
        print("✅ No errors detected.")
        return

    for idx, e in enumerate(errors, 1):
        line = f"Line {e['line']}" if e['line'] else "Line unknown"
        print(f"{idx}. [{e['type']}] {line}")
        print(f"   → {e['description']}")

def print_explanation(text):
    print("\n🧠 Explanation:")
    print("-" * 40)
    print(text)
    print("-" * 40)

# 🔴 INPUT CODE
original_code = '''
import math

def calculate_average(numbers)
    total = 0
    count = len(numbers)

    for i in range(count):
        total += numbers[i]

    avg = total / count
    return avg


def factorial(n):
    if n < 0:
        return None
    result = 1
    for i in range(1, n):
        result *= i
    return result


def find_max_value(values):
    max_value = 0
    for v in values:
        if v > max_value:
            max_value = v
    return max_value


def divide_numbers(a, b):
    return a / b


def process_data(data):
    processed = []

    for item in data:
        if type(item) == int:
            processed.append(item * 2)
        elif type(item) == str:
            processed.append(item + 1)
        else:
            processed.append(item)

    return processed


def print_user_info(user):
    print("Name:", user["name"])
    print("Age:", user["age"])
    print("Email:", user["email"])


def main():
    numbers = [10, 20, 30, 40]
    empty_list = []

    print("Average:", calculate_average(numbers))
    print("Average empty:", calculate_average(empty_list))

    print("Factorial of 5:", factorial(5))
    print("Factorial of -1:", factorial(-1))

    print("Max value:", find_max_value(numbers))
    print("Max empty:", find_max_value(empty_list))

    print("Division:", divide_numbers(10, 0))

    mixed_data = [1, "hello", 3.5]
    print("Processed data:", process_data(mixed_data))

    user = {
        "name": "Alice",
        "age": 25
    }
    print_user_info(user)

    if numbers > 3:
        print("Numbers list is large")

    for i in range(5)
        print(i)


main()

'''

result = debug_code(original_code)

print("\n🚀 AGENTIC DEBUGGER REPORT")
print("=" * 50)

print_code_block("Original Code", original_code.strip())

print("\n🔍 Detected Issues")
print_errors(result["detected_errors"])

if result["status"] == "FIXED":
    print_code_block("Fixed Code", result["final_code"])

    explanation = result["fix_attempts"][-1]["explanation"]
    print_explanation(explanation)

    print("\n✅ Status: Code fixed successfully")

elif result["status"] == "NO_ERRORS":
    print("\n✅ Status: No errors found")

else:
    print("\n❌ Status: Unable to fix the code")
