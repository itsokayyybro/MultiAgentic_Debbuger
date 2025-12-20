from agentic_debugger.orchestrator import debug_code

code = '''
print(" )
'''

result = debug_code(code)
print(result)
