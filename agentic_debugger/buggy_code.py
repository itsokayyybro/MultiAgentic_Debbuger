"""
Example Buggy Code

This file contains intentional errors for the debugger to fix.
Includes syntax, runtime, and logical errors.
"""

BUGGY_CODE = '''
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

# Simple example with just one error
SIMPLE_BUGGY_CODE = '''
def greet(name)
    print(f"Hello, {name}!")

greet("World")
'''

if __name__ == "__main__":
    print("Example buggy code files")
    print(f"Main example: {len(BUGGY_CODE)} chars, multiple errors")
    print(f"Simple example: {len(SIMPLE_BUGGY_CODE)} chars, one error")