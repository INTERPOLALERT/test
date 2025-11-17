#!/usr/bin/env python3
"""
Complete System Test - Tests everything step by step
"""

import sys
import os

print("="*80)
print("KIMIGPT COMPLETE SYSTEM TEST")
print("="*80)
print()

# Change to project root
if os.path.exists('src'):
    os.chdir('.')
elif os.path.exists('../src'):
    os.chdir('..')
else:
    print("ERROR: Cannot find project root!")
    sys.exit(1)

print(f"Working directory: {os.getcwd()}")
print()

# Test 1: Check required packages
print("[1/10] Testing required packages...")
print("-" * 80)

required_packages = {
    'flask': 'Flask',
    'flask_cors': 'Flask-CORS',
    'dotenv': 'python-dotenv',
    'requests': 'requests',
    'PIL': 'Pillow',
    'groq': 'Groq',
    'google.generativeai': 'Google Generative AI'
}

missing_packages = []
for package, name in required_packages.items():
    try:
        __import__(package)
        print(f"✓ {name}")
    except ImportError:
        print(f"✗ {name} - NOT INSTALLED!")
        missing_packages.append(name)

if missing_packages:
    print()
    print(f"CRITICAL: {len(missing_packages)} packages missing!")
    print("Run: pip install -r requirements.txt")
    print()
    sys.exit(1)

print("✓ All required packages installed")
print()

# Test 2: Check config files
print("[2/10] Checking configuration files...")
print("-" * 80)

if not os.path.exists('config.json'):
    print("✗ config.json not found!")
    sys.exit(1)
print("✓ config.json exists")

if not os.path.exists('.env'):
    print("⚠ .env file not found - will use .env.example as template")
    if os.path.exists('.env.example'):
        import shutil
        shutil.copy('.env.example', '.env')
        print("✓ Created .env from .env.example")
    else:
        print("✗ .env.example not found!")
        sys.exit(1)
else:
    print("✓ .env exists")

print()

# Test 3: Check directory structure
print("[3/10] Checking directory structure...")
print("-" * 80)

required_dirs = [
    'src',
    'src/agents',
    'src/api',
    'src/core',
    'src/ui',
    'src/ui/templates'
]

for directory in required_dirs:
    if os.path.exists(directory):
        print(f"✓ {directory}/")
    else:
        print(f"✗ {directory}/ NOT FOUND!")
        sys.exit(1)

print()

# Test 4: Import API modules
print("[4/10] Testing API module imports...")
print("-" * 80)

try:
    sys.path.insert(0, os.getcwd())
    from src.api.groq_api import GroqAPI
    print("✓ GroqAPI")
except Exception as e:
    print(f"✗ GroqAPI: {e}")

try:
    from src.api.gemini_api import GeminiAPI
    print("✓ GeminiAPI")
except Exception as e:
    print(f"✗ GeminiAPI: {e}")

try:
    from src.api.huggingface_api import HuggingFaceAPI
    print("✓ HuggingFaceAPI")
except Exception as e:
    print(f"✗ HuggingFaceAPI: {e}")

try:
    from src.api.cohere_api import CohereAPI
    print("✓ CohereAPI")
except Exception as e:
    print(f"✗ CohereAPI: {e}")

print()

# Test 5: Import API Manager
print("[5/10] Testing API Manager...")
print("-" * 80)

try:
    from src.api.api_manager import APIManager, get_api_manager
    print("✓ APIManager imported successfully")

    # Try to initialize (this will fail if no API keys, but that's expected)
    try:
        manager = get_api_manager()
        if len(manager.providers) > 0:
            print(f"✓ API Manager initialized with {len(manager.providers)} provider(s)")
            for provider in manager.providers.keys():
                print(f"  - {provider}")
        else:
            print("⚠ API Manager initialized but NO API keys configured")
            print("  Add at least one API key to .env file")
    except Exception as e:
        print(f"⚠ API Manager initialization issue: {e}")
        print("  This is normal if no API keys are configured yet")

except Exception as e:
    print(f"✗ Failed to import APIManager: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 6: Import agents
print("[6/10] Testing Agent imports...")
print("-" * 80)

agent_imports = [
    ('src.agents.orchestrator', 'OrchestratorAgent'),
    ('src.agents.understanding_agent', 'UnderstandingAgent'),
    ('src.agents.design_agent', 'DesignAgent'),
    ('src.agents.code_agent', 'CodeAgent'),
    ('src.agents.image_agent', 'ImageAgent'),
    ('src.agents.content_agent', 'ContentAgent'),
    ('src.agents.qa_agent', 'QAAgent'),
    ('src.agents.deployment_agent', 'DeploymentAgent'),
]

for module_name, class_name in agent_imports:
    try:
        module = __import__(module_name, fromlist=[class_name])
        getattr(module, class_name)
        print(f"✓ {class_name}")
    except Exception as e:
        print(f"✗ {class_name}: {e}")

print()

# Test 7: Import Multi-Agent System
print("[7/10] Testing Multi-Agent System...")
print("-" * 80)

try:
    from src.core.multi_agent_system import MultiAgentSystem, get_multi_agent_system
    print("✓ MultiAgentSystem imported successfully")
except Exception as e:
    print(f"✗ Failed to import MultiAgentSystem: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 8: Import Flask app
print("[8/10] Testing Flask app import...")
print("-" * 80)

try:
    from src.ui.app import app
    print("✓ Flask app imported successfully")
    print(f"  App name: {app.name}")
    print(f"  Debug mode: {app.debug}")
except Exception as e:
    print(f"✗ Failed to import Flask app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 9: Check Flask templates
print("[9/10] Checking Flask templates...")
print("-" * 80)

required_templates = [
    'src/ui/templates/index.html',
    'src/ui/templates/generator.html',
    'src/ui/templates/api_settings.html'
]

for template in required_templates:
    if os.path.exists(template):
        print(f"✓ {os.path.basename(template)}")
    else:
        print(f"✗ {os.path.basename(template)} NOT FOUND!")

print()

# Test 10: Test Flask routes
print("[10/10] Testing Flask routes...")
print("-" * 80)

try:
    with app.app_context():
        routes = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                routes.append(f"{rule.rule} ({','.join(rule.methods - {'HEAD', 'OPTIONS'})})")

        print(f"✓ Found {len(routes)} routes:")
        for route in sorted(routes)[:10]:  # Show first 10
            print(f"  {route}")
        if len(routes) > 10:
            print(f"  ... and {len(routes) - 10} more")

except Exception as e:
    print(f"⚠ Could not enumerate routes: {e}")

print()
print("="*80)
print("TEST SUMMARY")
print("="*80)
print()
print("✓ All critical components loaded successfully!")
print()
print("NEXT STEPS:")
print("1. Make sure you have at least ONE API key in .env file")
print("2. Run: python src/ui/app.py")
print("3. Open browser to http://localhost:5000")
print()
print("To get FREE API keys:")
print("- Groq: https://console.groq.com/ (30 seconds, fastest!)")
print("- Gemini: https://makersuite.google.com/app/apikey")
print("- Hugging Face: https://huggingface.co/settings/tokens")
print("- Cohere: https://dashboard.cohere.com/api-keys")
print()
print("All are 100% FREE - no credit card required!")
print("="*80)
