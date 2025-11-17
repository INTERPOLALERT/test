# KimiGPT Installation Fix Guide

## 🔴 App Not Working? Follow These Steps IN ORDER

---

## STEP 1: Check Python Version

```bash
python --version
```

**YOU MUST HAVE Python 3.7 - 3.11**

- ❌ Python 3.6 or older: TOO OLD - Install Python 3.8-3.11
- ✅ Python 3.7, 3.8, 3.9, 3.10, 3.11: PERFECT
- ⚠️ Python 3.12 or newer: May have issues, use 3.8-3.11

**Download Python:** https://www.python.org/downloads/

---

## STEP 2: Run Diagnostic Tests

```bash
cd kimigpt

# Test 1: Complete system test
python test_system.py

# Test 2: Minimal Flask test
python test_flask_minimal.py
```

**What these tests do:**
- `test_system.py` - Checks everything (packages, files, imports)
- `test_flask_minimal.py` - Tests if Flask can start at all

**If test_flask_minimal.py works:** The problem is with API keys or configuration
**If test_flask_minimal.py fails:** The problem is with Python/Flask installation

---

## STEP 3: Fresh Installation (NUCLEAR OPTION)

If tests fail, do a complete fresh install:

```bash
cd kimigpt

# 1. Delete virtual environment
rmdir /s /q venv

# 2. Delete .env file
del .env

# 3. Create fresh virtual environment
python -m venv venv

# 4. Activate it
venv\Scripts\activate

# 5. Upgrade pip
python -m pip install --upgrade pip

# 6. Install requirements
pip install -r requirements.txt

# 7. Copy .env example
copy .env.example .env

# 8. Edit .env and add at least ONE API key
notepad .env
```

---

## STEP 4: Get FREE API Keys

You need AT LEAST ONE API key. All are 100% FREE:

### Option A: Groq (FASTEST - Recommended!)
1. Go to: https://console.groq.com/
2. Sign up (30 seconds, no credit card)
3. Click "API Keys" → "Create API Key"
4. Copy the key (starts with `gsk_...`)
5. Add to .env: `GROQ_API_KEY=gsk_your_key_here`

### Option B: Google Gemini
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click "Get API Key" → "Create API key in new project"
4. Copy the key (starts with `AIzaSy...`)
5. Add to .env: `GEMINI_API_KEY=AIzaSy_your_key_here`

### Option C: Hugging Face
1. Go to: https://huggingface.co/settings/tokens
2. Sign up (no credit card)
3. Click "New token" → Name it "KimiGPT"
4. Copy the token (starts with `hf_...`)
5. Add to .env: `HUGGINGFACE_API_KEY=hf_your_token_here`

### Option D: Cohere
1. Go to: https://dashboard.cohere.com/api-keys
2. Sign up (no credit card)
3. Copy the API key
4. Add to .env: `COHERE_API_KEY=your_key_here`

---

## STEP 5: Test Again

```bash
# Activate virtual environment
venv\Scripts\activate

# Run system test
python test_system.py

# If all tests pass, start KimiGPT
startgpt.bat
```

---

## COMMON ERRORS & FIXES

### Error: "ModuleNotFoundError: No module named 'flask'"

**Problem:** Requirements not installed

**Fix:**
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

---

### Error: "ERR_CONNECTION_REFUSED" in browser

**Causes & Fixes:**

**1. Flask Not Started Yet**
- Wait 5 seconds after running `startgpt.bat`
- Browser opens too fast, Flask still starting

**2. Flask Crashed on Startup**
- Look at the console where you ran `startgpt.bat`
- Check for error messages
- Run `python test_system.py` to diagnose

**3. Port 5000 Already in Use**
```bash
# Windows: Find what's using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Or change port in .env
# Edit .env and set: FLASK_PORT=8000
```

**4. Firewall Blocking**
- Open Windows Defender Firewall
- Click "Allow an app through firewall"
- Find Python and check both Private and Public
- Click OK and try again

**5. No API Keys Configured**
- Flask starts but crashes immediately
- Check console for "No API providers available"
- Add at least ONE API key to .env file

---

### Error: "Could not find a version that satisfies the requirement opencv-python"

**Problem:** OLD requirements.txt with bloated dependencies

**Fix:**
```bash
# Get latest version
cd kimigpt
git pull origin claude/kimigpt-011CV1sqvvnTJkpEfDiLJXfb

# Reinstall
venv\Scripts\activate
pip install -r requirements.txt --force-reinstall
```

The new requirements.txt has ONLY 7 packages (was 30+) and works with Python 3.7-3.12.

---

### Error: "Permission denied" or "Access denied"

**Fix:**
1. Close all Python processes
2. Right-click `installgpt.bat`
3. Choose "Run as administrator"

---

### Error: "python is not recognized"

**Problem:** Python not installed or not in PATH

**Fix:**
1. Install Python from https://www.python.org/downloads/
2. **IMPORTANT:** Check "Add Python to PATH" during installation
3. Restart Command Prompt
4. Test: `python --version`

---

## VERIFICATION CHECKLIST

Before reporting issues, verify:

- [ ] Python 3.7-3.11 installed: `python --version`
- [ ] Virtual environment created: `venv` folder exists
- [ ] Requirements installed: `pip list | grep flask`
- [ ] .env file exists and has at least ONE API key
- [ ] `test_system.py` passes all tests
- [ ] `test_flask_minimal.py` opens successfully in browser
- [ ] Port 5000 is not used by another app
- [ ] Firewall allows Python
- [ ] No antivirus blocking Python
- [ ] Running from `kimigpt` directory

---

## MANUAL STEP-BY-STEP TEST

If everything else fails, test manually:

```bash
# 1. Go to kimigpt directory
cd kimigpt

# 2. Check files exist
dir src
dir src\ui
dir src\api

# 3. Activate venv
venv\Scripts\activate

# 4. Test Python
python --version

# 5. Test Flask
python -c "import flask; print('Flask OK')"

# 6. Test imports
python -c "from src.ui.app import app; print('App imports OK')"

# 7. Start Flask manually
python src\ui\app.py
```

Watch the console for errors at each step.

---

## STILL NOT WORKING?

### Option 1: Use Test Scripts

```bash
# Test if Flask works at all
python test_flask_minimal.py

# If that works, test full system
python test_system.py
```

### Option 2: Check Windows Hosts File

Sometimes localhost is broken:

```bash
# Open hosts file
notepad C:\Windows\System32\drivers\etc\hosts

# Make sure this line exists:
127.0.0.1       localhost
```

### Option 3: Try Different Port

Edit `.env`:
```
FLASK_PORT=8000
```

Then use: http://localhost:8000

### Option 4: Check Antivirus

Some antivirus software blocks Python web servers:
1. Temporarily disable antivirus
2. Try starting KimiGPT again
3. If it works, add exception for Python

---

## NUCLEAR OPTION: Complete Reinstall

```bash
# 1. Delete everything
cd kimigpt
rmdir /s /q venv
del .env
del *.db

# 2. Get latest code
git pull origin claude/kimigpt-011CV1sqvvnTJkpEfDiLJXfb

# 3. Reinstall from scratch
installgpt.bat

# 4. Add API keys when prompted

# 5. Test
python test_system.py

# 6. Start
startgpt.bat
```

---

## EXPECTED WORKING BEHAVIOR

When everything is working correctly:

1. Run `startgpt.bat`
2. Console shows:
   ```
   ✓ Python OK
   ✓ Virtual Environment OK
   ✓ Configuration OK
   ✓ Virtual Environment Activated
   ✓ Dependencies OK
   [Testing API Connections...]
   ```
3. Flask starts:
   ```
   * Running on http://0.0.0.0:5000
   ```
4. Browser opens automatically after 5 seconds
5. Dashboard appears with "Generate Website" button
6. No errors in console

---

## GET HELP

If none of this works:

1. Run: `python test_system.py` and save the output
2. Run: `python test_flask_minimal.py` and note what happens
3. Copy any error messages from the console
4. Check Python version: `python --version`
5. Check if Flask installed: `pip list | findstr flask`
6. Check if .env has API key: `type .env | findstr API_KEY`

Include all this information when asking for help!

---

## Quick Reference

```bash
# Complete diagnosis
python diagnose.py

# Test system
python test_system.py

# Test minimal Flask
python test_flask_minimal.py

# Fresh install
installgpt.bat

# Start app
startgpt.bat

# Manual start (for debugging)
venv\Scripts\activate
python src\ui\app.py
```
