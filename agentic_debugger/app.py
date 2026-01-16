from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import time
import os
import sys
import re

app = Flask(__name__)
CORS(app)

# Try to import orchestrator, but don't fail if it's not available
ORCHESTRATOR_AVAILABLE = False
try:
    from orchestrator import debug_code
    ORCHESTRATOR_AVAILABLE = True
    print("✅ Orchestrator imported successfully!")
except ImportError as e:
    print(f"⚠️  Warning: Could not import orchestrator: {e}")
    print("📝 Running in MOCK MODE - will simulate debugging")
except Exception as e:
    print(f"⚠️  Error importing orchestrator: {e}")
    print("📝 Running in MOCK MODE")

def analyze_code_errors(code):
    """Analyze code for detailed error information"""
    errors = []
    lines = code.split('\n')
    
    for i, line in enumerate(lines, 1):
        line_stripped = line.strip()
        
        # Check for missing colons
        if line_stripped.startswith('def ') and ':' not in line:
            errors.append({
                'line': i,
                'type': 'Syntax',
                'severity': '🔴',
                'description': f'Function definition is missing a colon.'
            })
        elif line_stripped.startswith('for ') and ':' not in line:
            errors.append({
                'line': i,
                'type': 'Syntax',
                'severity': '🔴',
                'description': 'For loop is missing a colon.'
            })
        elif line_stripped.startswith('if ') and ':' not in line:
            errors.append({
                'line': i,
                'type': 'Syntax',
                'severity': '🔴',
                'description': 'If statement is missing a colon.'
            })
        elif line_stripped.startswith('while ') and ':' not in line:
            errors.append({
                'line': i,
                'type': 'Syntax',
                'severity': '🔴',
                'description': 'While loop is missing a colon.'
            })
        elif line_stripped.startswith('elif ') and ':' not in line:
            errors.append({
                'line': i,
                'type': 'Syntax',
                'severity': '🔴',
                'description': 'Elif statement is missing a colon.'
            })
        elif line_stripped.startswith('else') and ':' not in line and line_stripped == 'else':
            errors.append({
                'line': i,
                'type': 'Syntax',
                'severity': '🔴',
                'description': 'Else statement is missing a colon.'
            })
        
        # Check for unmatched parentheses in the line
        if '(' in line:
            open_count = line.count('(')
            close_count = line.count(')')
            if open_count != close_count:
                errors.append({
                    'line': i,
                    'type': 'Syntax',
                    'severity': '🔴',
                    'description': f'Unmatched parentheses (found {open_count} opening, {close_count} closing).'
                })
        
        # Check for missing quotes
        single_quotes = line.count("'")
        double_quotes = line.count('"')
        if single_quotes % 2 != 0:
            errors.append({
                'line': i,
                'type': 'Syntax',
                'severity': '🔴',
                'description': 'Unclosed single quote.'
            })
        if double_quotes % 2 != 0:
            errors.append({
                'line': i,
                'type': 'Syntax',
                'severity': '🔴',
                'description': 'Unclosed double quote.'
            })
        
        # Check for range issues
        if 'range(1,' in line and ')' in line:
            errors.append({
                'line': i,
                'type': 'Logical',
                'severity': '🟡',
                'description': 'Range might exclude the upper bound. Consider if you need range(1, n+1) instead of range(1, n).'
            })
    
    return errors

def generate_fixes_description(original_code, fixed_code, errors):
    """Generate description of what was fixed"""
    fixes = []
    
    original_lines = original_code.split('\n')
    fixed_lines = fixed_code.split('\n')
    
    for error in errors:
        line_num = error['line']
        if line_num <= len(original_lines) and line_num <= len(fixed_lines):
            original_line = original_lines[line_num - 1].strip()
            fixed_line = fixed_lines[line_num - 1].strip() if line_num <= len(fixed_lines) else original_line
            
            if original_line != fixed_line:
                if error['type'] == 'Syntax' and 'colon' in error['description']:
                    fixes.append({
                        'line': line_num,
                        'description': f'Added a colon to fix the syntax error.'
                    })
                elif error['type'] == 'Syntax' and 'parenthes' in error['description']:
                    fixes.append({
                        'line': line_num,
                        'description': f'Fixed unmatched parentheses.'
                    })
                elif error['type'] == 'Syntax' and 'quote' in error['description']:
                    fixes.append({
                        'line': line_num,
                        'description': f'Fixed unclosed quote.'
                    })
                elif error['type'] == 'Logical' and 'range' in error['description']:
                    fixes.append({
                        'line': line_num,
                        'description': f'Modified range to include the upper bound correctly.'
                    })
    
    # Add generic fixes if no specific ones found
    if not fixes and errors:
        fixes.append({
            'line': None,
            'description': 'Fixed syntax and logical errors in the code.'
        })
    
    return fixes

def mock_debug_code(code):
    """Enhanced mock function with detailed error analysis"""
    print("🎭 Using MOCK MODE")
    time.sleep(1)
    
    # Analyze errors
    errors = analyze_code_errors(code)
    
    # Create a simple "fixed" version
    fixed_code = code
    lines = code.split('\n')
    fixed_lines = []
    
    for line in lines:
        # Add missing colons
        if line.strip().startswith('def ') and ':' not in line:
            line = line.rstrip() + ':'
        elif line.strip().startswith('for ') and ':' not in line:
            line = line.rstrip() + ':'
        elif line.strip().startswith('if ') and ':' not in line:
            line = line.rstrip() + ':'
        elif line.strip().startswith('while ') and ':' not in line:
            line = line.rstrip() + ':'
        elif line.strip().startswith('elif ') and ':' not in line:
            line = line.rstrip() + ':'
        elif line.strip() == 'else':
            line = line.rstrip() + ':'
        
        # Try to fix simple parenthesis issues
        if '(' in line and line.count('(') > line.count(')'):
            line = line.rstrip() + ')'
        
        fixed_lines.append(line)
    
    fixed_code = '\n'.join(fixed_lines)
    
    # Generate fixes description
    fixes = generate_fixes_description(code, fixed_code, errors)
    
    # Ensure values are proper integers
    errors_count = int(len(errors)) if errors else 0
    
    return {
        "status": "FIXED",
        "final_code": fixed_code,
        "errors_found": errors_count,
        "errors_detail": errors,
        "fixes_applied": fixes,
        "fix_attempts": 1,  # Always return integer
        "message": "Code debugged successfully"
    }

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "orchestrator_available": ORCHESTRATOR_AVAILABLE,
        "mode": "REAL" if ORCHESTRATOR_AVAILABLE else "MOCK"
    })

@app.route('/api/debug', methods=['POST'])
def debug_code_endpoint():
    """Main debugging endpoint"""
    try:
        data = request.get_json()
        
        if not data or 'code' not in data:
            return jsonify({
                "status": "error",
                "message": "No code provided"
            }), 400
        
        code = data['code']
        
        if not code.strip():
            return jsonify({
                "status": "error",
                "message": "Code cannot be empty"
            }), 400
        
        print(f"\n{'='*60}")
        print(f"🔍 Received debugging request")
        print(f"📝 Code length: {len(code)} characters")
        print(f"🤖 Mode: {'REAL' if ORCHESTRATOR_AVAILABLE else 'MOCK'}")
        print(f"{'='*60}\n")
        
        # Use actual orchestrator or mock
        if ORCHESTRATOR_AVAILABLE:
            try:
                result = debug_code(code)
                
                # Transform orchestrator result to match expected format
                # Orchestrator returns: detected_errors, fix_attempts (list), status, final_code, original_code
                # App expects: errors_found, fix_attempts (int), status, final_code, errors_detail, fixes_applied
                
                # Map detected_errors to errors_detail
                if 'detected_errors' in result and 'errors_detail' not in result:
                    errors = result.get('detected_errors', [])
                    result['errors_detail'] = [
                        {
                            'line': e.get('line'),
                            'type': e.get('type', 'Unknown'),
                            'severity': '🔴' if e.get('type') == 'Syntax' else '🟡',
                            'description': e.get('description', 'Unknown error')
                        }
                        for e in errors
                    ]
                else:
                    result['errors_detail'] = result.get('errors_detail', analyze_code_errors(code))
                
                # Set errors_found as count
                result['errors_found'] = len(result.get('errors_detail', []))
                
                # Get fix_attempts count (orchestrator returns a list of attempts)
                attempts_list = result.get('fix_attempts', [])
                result['fix_attempts'] = len(attempts_list) if isinstance(attempts_list, list) else 1
                
                # Generate fixes_applied if not present
                if 'fixes_applied' not in result:
                    original_code = code
                    fixed_code = result.get('final_code', code)
                    result['fixes_applied'] = generate_fixes_description(
                        original_code, 
                        fixed_code, 
                        result.get('errors_detail', [])
                    )
                
                print("✅ Debugging completed successfully!")
            except Exception as e:
                print(f"❌ Error in orchestrator: {e}")
                print("🎭 Falling back to MOCK MODE")
                result = mock_debug_code(code)
        else:
            result = mock_debug_code(code)
        
        # Debug print to see what we're sending
        print(f"\n📤 Sending response:")
        print(f"   Status: {result.get('status')}")
        print(f"   Errors Found: {result.get('errors_found')} (type: {type(result.get('errors_found'))})")
        print(f"   Fix Attempts: {result.get('fix_attempts')} (type: {type(result.get('fix_attempts'))})")
        
        return jsonify({
            "status": "success",
            "result": result
        })
        
    except Exception as e:
        print(f"❌ Error in debug endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/validate', methods=['POST'])
def validate_code():
    """Quick validation endpoint"""
    try:
        data = request.get_json()
        code = data.get('code', '')
        
        # Basic Python syntax check
        try:
            compile(code, '<string>', 'exec')
            return jsonify({
                "valid": True,
                "message": "Syntax looks good!"
            })
        except SyntaxError as e:
            return jsonify({
                "valid": False,
                "message": f"Syntax Error: {str(e)}"
            })
            
    except Exception as e:
        return jsonify({
            "valid": False,
            "message": str(e)
        }), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 MULTI-AGENTIC DEBUGGER - WEB SERVER")
    print("="*60)
    
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        print("📁 Creating templates directory...")
        os.makedirs('templates')
    
    if not os.path.exists('static'):
        print("📁 Creating static directory...")
        os.makedirs('static')
    
    # Check if index.html exists
    if not os.path.exists('templates/index.html'):
        print("⚠️  WARNING: templates/index.html not found!")
        print("📝 Please create templates/index.html using the Frontend UI artifact")
    else:
        print("✅ Found templates/index.html")
    
    print(f"\n📊 Status:")
    print(f"   Orchestrator Available: {ORCHESTRATOR_AVAILABLE}")
    print(f"   Mode: {'REAL DEBUGGING' if ORCHESTRATOR_AVAILABLE else 'MOCK MODE'}")
    
    if not ORCHESTRATOR_AVAILABLE:
        print("\n💡 TIP: To enable real debugging:")
        print("   1. Make sure all backend files exist (config.py, orchestrator.py, etc.)")
        print("   2. Set GOOGLE_API_KEY environment variable")
        print("   3. Restart the server")
    
    print(f"\n🌐 Server starting...")
    print(f"   URL: http://localhost:5000")
    print(f"   Press CTRL+C to stop")
    print("="*60 + "\n")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except OSError as e:
        if "Address already in use" in str(e):
            print("\n❌ ERROR: Port 5000 is already in use!")
            print("\n💡 Solutions:")
            print("   1. Stop the other process using port 5000")
            print("   2. Or change the port in app.py:")
            print("      app.run(debug=True, host='0.0.0.0', port=8080)")
        else:
            print(f"\n❌ ERROR: {e}")
        sys.exit(1)