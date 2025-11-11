#!/usr/bin/env python3
"""
KimiGPT - Diagnostic Tool
Checks your system for common issues
"""

import sys
import os

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def check_python_version():
    """Check Python version"""
    print_section("PYTHON VERSION CHECK")

    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.patch}"

    print(f"✓ Python Version: {version_str}")
    print(f"  Location: {sys.executable}")

    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("\n❌ ERROR: Python 3.7+ is required!")
        print("   Current version is too old.")
        return False
    elif version.major == 3 and version.minor >= 12:
        print("\n⚠️  WARNING: Python 3.12+ detected")
        print("   Some packages may have limited support.")
        print("   Recommended: Python 3.8-3.11")
        return True
    else:
        print(f"\n✓ Python version is compatible!")
        return True

def check_packages():
    """Check if required packages are installed"""
    print_section("PACKAGE CHECK")

    required_packages = {
        'flask': 'Flask Web Framework',
        'flask_cors': 'Flask CORS Support',
        'requests': 'HTTP Library',
        'dotenv': 'Environment Variables (python-dotenv)',
        'PIL': 'Image Processing (Pillow)',
        'groq': 'Groq API',
        'google.generativeai': 'Google Gemini API',
        'rich': 'Terminal UI (for testing)'
    }

    all_ok = True

    for package, description in required_packages.items():
        try:
            __import__(package)
            print(f"✓ {description}: Installed")
        except ImportError:
            print(f"❌ {description}: NOT FOUND")
            all_ok = False

    if not all_ok:
        print("\n⚠️  MISSING PACKAGES DETECTED")
        print("   Run: pip install -r requirements.txt")
    else:
        print("\n✓ All required packages installed!")

    return all_ok

def check_env_file():
    """Check .env file"""
    print_section("CONFIGURATION CHECK")

    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("   Run installgpt.bat or copy .env.example to .env")
        return False

    print("✓ .env file exists")

    # Check for API keys
    api_keys_found = []
    with open('.env', 'r') as f:
        content = f.read()
        if 'GROQ_API_KEY=' in content and 'your-key-here' not in content:
            api_keys_found.append('Groq')
        if 'GEMINI_API_KEY=' in content and 'your-key-here' not in content:
            api_keys_found.append('Gemini')
        if 'HUGGINGFACE_API_KEY=' in content and 'your-token-here' not in content:
            api_keys_found.append('Hugging Face')
        if 'COHERE_API_KEY=' in content and 'your-key-here' not in content:
            api_keys_found.append('Cohere')

    if api_keys_found:
        print(f"✓ Found API keys: {', '.join(api_keys_found)}")
        return True
    else:
        print("⚠️  No API keys configured")
        print("   Add at least one API key to .env file")
        print("   See api.txt for instructions")
        return False

def check_directory_structure():
    """Check if required directories exist"""
    print_section("DIRECTORY STRUCTURE CHECK")

    required_dirs = [
        'src/agents',
        'src/api',
        'src/core',
        'src/ui',
        'src/ui/templates'
    ]

    all_ok = True
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✓ {directory}")
        else:
            print(f"❌ {directory} NOT FOUND")
            all_ok = False

    return all_ok

def test_flask_import():
    """Test if Flask app can be imported"""
    print_section("FLASK APP CHECK")

    try:
        sys.path.insert(0, os.getcwd())
        from src.ui import app
        print("✓ Flask app imports successfully")
        return True
    except Exception as e:
        print(f"❌ Flask app import failed:")
        print(f"   Error: {e}")
        return False

def main():
    """Run all diagnostics"""
    print("\n" + "█"*60)
    print("  KIMIGPT DIAGNOSTIC TOOL")
    print("  Checking your installation...")
    print("█"*60)

    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    results = {
        'Python Version': check_python_version(),
        'Packages': check_packages(),
        'Configuration': check_env_file(),
        'Directory Structure': check_directory_structure(),
        'Flask App': test_flask_import()
    }

    print_section("SUMMARY")

    passed = sum(results.values())
    total = len(results)

    for check, result in results.items():
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status} - {check}")

    print(f"\nScore: {passed}/{total} checks passed")

    if passed == total:
        print("\n🎉 All checks passed! Your installation looks good!")
        print("   Run startgpt.bat to start KimiGPT")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nCOMMON FIXES:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Configure API keys: Edit .env file (see api.txt)")
        print("3. Check Python version: python --version (need 3.7+)")
        print("4. Make sure you're in the kimigpt directory")

    print("\n" + "="*60 + "\n")

    return 0 if passed == total else 1

if __name__ == '__main__':
    sys.exit(main())
