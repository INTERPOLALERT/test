#!/usr/bin/env python3
"""
Minimal Flask Test - Tests if Flask can start at all
"""

print("="*80)
print("MINIMAL FLASK TEST")
print("="*80)
print()

# Test 1: Can we import Flask?
print("[1/3] Testing Flask import...")
try:
    from flask import Flask
    print("✓ Flask imported successfully")
except ImportError as e:
    print("✗ Flask not installed!")
    print(f"Error: {e}")
    print()
    print("FIX: Run this command:")
    print("pip install flask")
    exit(1)

print()

# Test 2: Can we create a Flask app?
print("[2/3] Creating minimal Flask app...")
try:
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return '''
        <html>
        <head><title>KimiGPT Test</title></head>
        <body style="font-family: Arial; padding: 50px; text-align: center;">
            <h1 style="color: green;">✓ Flask is Working!</h1>
            <p>If you can see this, Flask is starting correctly.</p>
            <p>KimiGPT should work now.</p>
            <hr>
            <p><a href="/test">Test another route</a></p>
        </body>
        </html>
        '''

    @app.route('/test')
    def test():
        return '''
        <html>
        <head><title>Test Route</title></head>
        <body style="font-family: Arial; padding: 50px; text-align: center;">
            <h1 style="color: blue;">✓ Routes Work!</h1>
            <p>Flask routing is working correctly.</p>
            <p><a href="/">Go back</a></p>
        </body>
        </html>
        '''

    print("✓ Flask app created successfully")
except Exception as e:
    print(f"✗ Failed to create Flask app: {e}")
    exit(1)

print()

# Test 3: Start the server
print("[3/3] Starting Flask server...")
print("="*80)
print()
print("If Flask starts successfully, you will see:")
print('  * Running on http://127.0.0.1:5000')
print()
print("Then open your browser to: http://localhost:5000")
print()
print("If you see a green checkmark, Flask is working!")
print("Press Ctrl+C to stop the server")
print()
print("="*80)
print()

try:
    app.run(host='0.0.0.0', port=5000, debug=True)
except KeyboardInterrupt:
    print("\n\nServer stopped by user")
except Exception as e:
    print(f"\n✗ ERROR: Flask failed to start!")
    print(f"Error: {e}")
    print()
    print("POSSIBLE CAUSES:")
    print("1. Port 5000 is already in use")
    print("   - Close other applications using port 5000")
    print("   - Or change port in .env file: FLASK_PORT=8000")
    print()
    print("2. Firewall is blocking Python")
    print("   - Allow Python in Windows Firewall")
    print()
    print("3. Permission denied")
    print("   - Run as Administrator")
    exit(1)
