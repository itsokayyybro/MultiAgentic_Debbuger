#!/usr/bin/env python3
"""
Automated setup script for Multi-Agentic Debugger Web Interface
Run this to quickly set up your web interface!
"""

import os
import sys
import subprocess

def print_header(text):
    """Print a fancy header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def run_command(cmd, description):
    """Run a shell command and handle errors"""
    print(f"⏳ {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                               capture_output=True, text=True)
        print(f"✅ {description} - Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed!")
        print(f"Error: {e.stderr}")
        return False

def check_file_exists(filepath):
    """Check if a file exists"""
    return os.path.isfile(filepath)

def create_directory(dirpath):
    """Create a directory if it doesn't exist"""
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
        print(f"✅ Created directory: {dirpath}")
    else:
        print(f"📁 Directory already exists: {dirpath}")

def main():
    print_header("🚀 Multi-Agentic Debugger - Web Setup")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ is required!")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")
    
    # Step 1: Check existing files
    print_header("Step 1: Checking Existing Files")
    
    required_files = [
        'config.py',
        'llm_client.py', 
        'prompts.py',
        'agents.py',
        'orchestrator.py'
    ]
    
    missing_files = []
    for file in required_files:
        if check_file_exists(file):
            print(f"✅ Found: {file}")
        else:
            print(f"⚠️  Missing: {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  Warning: Some backend files are missing.")
        print("The web interface will work in MOCK MODE only.")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            sys.exit(0)
    
    # Step 2: Create directories
    print_header("Step 2: Creating Directories")
    create_directory('templates')
    create_directory('static')
    
    # Step 3: Install dependencies
    print_header("Step 3: Installing Dependencies")
    
    if check_file_exists('requirements_flask.txt'):
        run_command('pip install -r requirements_flask.txt', 
                   'Installing Flask requirements')
    else:
        print("⚠️  requirements_flask.txt not found")
        print("Installing Flask manually...")
        run_command('pip install Flask flask-cors', 
                   'Installing Flask and CORS')
    
    # Step 4: Check for required files
    print_header("Step 4: Checking Web Interface Files")
    
    if not check_file_exists('app.py'):
        print("⚠️  app.py not found!")
        print("Please create app.py using the Flask Backend artifact")
    else:
        print("✅ Found: app.py")
    
    if not check_file_exists('templates/index.html'):
        print("⚠️  templates/index.html not found!")
        print("Please create templates/index.html using the Frontend UI artifact")
    else:
        print("✅ Found: templates/index.html")
    
    # Step 5: Check environment variables
    print_header("Step 5: Checking Environment Variables")
    
    api_key = os.environ.get('GOOGLE_API_KEY')
    if api_key:
        print(f"✅ GOOGLE_API_KEY is set (length: {len(api_key)})")
    else:
        print("⚠️  GOOGLE_API_KEY not set")
        print("You can still run in MOCK MODE or set it later")
    
    # Summary
    print_header("🎉 Setup Summary")
    
    all_good = True
    
    if check_file_exists('app.py'):
        print("✅ Backend API ready")
    else:
        print("❌ Backend API missing (app.py)")
        all_good = False
    
    if check_file_exists('templates/index.html'):
        print("✅ Frontend UI ready")
    else:
        print("❌ Frontend UI missing (templates/index.html)")
        all_good = False
    
    print("✅ Directories created")
    print("✅ Dependencies should be installed")
    
    if api_key:
        print("✅ API key configured")
    else:
        print("⚠️  API key not set (will use mock mode)")
    
    # Next steps
    print_header("📝 Next Steps")
    
    if not all_good:
        print("1. Create missing files:")
        if not check_file_exists('app.py'):
            print("   - Create app.py from the Flask Backend artifact")
        if not check_file_exists('templates/index.html'):
            print("   - Create templates/index.html from the Frontend UI artifact")
        print("2. Run this script again")
        print("3. Start the server with: python app.py")
    else:
        print("✅ Everything is ready!")
        print("\n🚀 To start the server, run:")
        print("   python app.py")
        print("\n🌐 Then open your browser to:")
        print("   http://localhost:5000")
        
        # Offer to start server
        response = input("\nWould you like to start the server now? (y/n): ")
        if response.lower() == 'y':
            print("\n🚀 Starting server...")
            try:
                subprocess.run(['python', 'app.py'])
            except KeyboardInterrupt:
                print("\n\n👋 Server stopped. Goodbye!")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled. Goodbye!")
        sys.exit(0)