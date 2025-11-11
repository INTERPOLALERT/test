# KimiGPT Troubleshooting Guide

This guide helps you fix common issues with KimiGPT installation and operation.

---

## 🔍 Quick Diagnosis

**Run the diagnostic tool first:**
```bash
python diagnose.py
```

This will check your Python version, packages, configuration, and more.

---

## ❌ PROBLEM: "ERR_CONNECTION_REFUSED" when opening localhost

### Symptoms
- Browser shows "This site can't be reached"
- "localhost refused to connect"
- ERR_CONNECTION_REFUSED

### Causes & Solutions

#### 1. Flask Installation Failed
**Check if Flask is installed:**
```bash
python -c "import flask"
```

If you get an error:
```bash
cd kimigpt
pip install -r requirements.txt
```

#### 2. Python Version Incompatibility
**Check your Python version:**
```bash
python --version
```

**Required: Python 3.7 - 3.11**
- ❌ Python 3.6 or older: **TOO OLD**
- ✅ Python 3.7 - 3.11: **PERFECT**
- ⚠️  Python 3.12+: **May have compatibility issues**

**Solution:** Install Python 3.8-3.11 from python.org

#### 3. Port Already in Use
**Someone else is using port 5000**

Check if another application is using the port:
```bash
# Windows
netstat -ano | findstr :5000

# Kill the process using the port (replace PID with actual number)
taskkill /PID <PID> /F
```

Or change the port in `.env`:
```
FLASK_PORT=8000
```

#### 4. Firewall Blocking
**Windows Firewall might be blocking Python**

Solution:
1. Open Windows Firewall settings
2. Allow Python through firewall
3. Try again

#### 5. Virtual Environment Issues
**Virtual environment might be corrupted**

```bash
cd kimigpt
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## ❌ PROBLEM: "Could not find a version that satisfies the requirement opencv-python==4.8.1"

### Solution
**We've fixed this!** Update to the latest version:

```bash
cd kimigpt
git pull origin claude/kimigpt-011CV1sqvvnTJkpEfDiLJXfb
pip install -r requirements.txt
```

**The new requirements.txt:**
- ✅ Removed opencv-python (not needed!)
- ✅ Removed 20+ unused packages
- ✅ Works with Python 3.7-3.12
- ✅ Installs in seconds, not minutes

---

## ❌ PROBLEM: "Module not found" errors

### Common errors:
```
ModuleNotFoundError: No module named 'flask'
ModuleNotFoundError: No module named 'groq'
ModuleNotFoundError: No module named 'google.generativeai'
```

### Solution
**Install dependencies:**
```bash
cd kimigpt
venv\Scripts\activate
pip install -r requirements.txt
```

**Still not working?**
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt --upgrade
```

---

## ❌ PROBLEM: Flask starts but shows errors in browser

### "No API providers available"

**You need to configure API keys!**

**Method 1: In-App (Easiest)**
1. Start KimiGPT: `startgpt.bat`
2. Click "⚙️ API Settings" on dashboard
3. Get API keys from links provided
4. Paste keys and click "Save"

**Method 2: Manual .env file**
1. Copy `.env.example` to `.env`
2. Edit `.env` file
3. Add at least ONE API key:
   ```
   GROQ_API_KEY=gsk_your_actual_key_here
   ```

**Get FREE API keys:**
- Groq: https://console.groq.com/ (30 seconds, NO credit card!)
- Gemini: https://makersuite.google.com/app/apikey
- Hugging Face: https://huggingface.co/settings/tokens
- Cohere: https://dashboard.cohere.com/api-keys

All 4 are 100% FREE - no credit card required!

---

## ❌ PROBLEM: "installgpt.bat failed"

### Check what went wrong:

```bash
# Run installation step by step manually:
cd kimigpt

# 1. Create virtual environment
python -m venv venv

# 2. Activate it
venv\Scripts\activate

# 3. Upgrade pip
python -m pip install --upgrade pip

# 4. Install requirements
pip install -r requirements.txt

# 5. Create .env
copy .env.example .env

# 6. Edit .env and add API keys
notepad .env
```

---

## ❌ PROBLEM: Browser opens but shows blank page

### Solution
1. **Clear browser cache:** Ctrl+Shift+Delete
2. **Try incognito mode:** Ctrl+Shift+N
3. **Try different browser:** Chrome, Firefox, Edge
4. **Check Flask logs** in the terminal for errors

---

## ❌ PROBLEM: "API request failed" errors

### Check API keys are valid:

**Method 1: Use API Settings page**
1. Go to http://localhost:5000/api-settings
2. Click "Test Connection" for each API
3. Fix any that show "Failed"

**Method 2: Check .env file**
```bash
notepad .env
```

Make sure keys are:
- ✅ Complete (not truncated)
- ✅ No extra spaces
- ✅ Correct format:
  - Groq: `gsk_...`
  - Gemini: `AIzaSy...`
  - Hugging Face: `hf_...`
  - Cohere: (no prefix)

---

## ❌ PROBLEM: "Permission denied" errors

### Windows

**Run as Administrator:**
1. Right-click `installgpt.bat`
2. Choose "Run as administrator"

---

## ❌ PROBLEM: Everything else

### Step-by-step full reinstall:

```bash
# 1. Delete everything except source code
cd kimigpt
rmdir /s venv
del .env
del *.db

# 2. Get latest version
git pull origin claude/kimigpt-011CV1sqvvnTJkpEfDiLJXfb

# 3. Reinstall
installgpt.bat

# 4. When prompted, add at least ONE API key

# 5. Start
startgpt.bat
```

---

## 🆘 Still Not Working?

### Run full diagnostics:
```bash
cd kimigpt
python diagnose.py
```

### Check logs:
- Look at terminal output when running `startgpt.bat`
- Flask will show detailed error messages

### Common quick fixes:
```bash
# 1. Make sure you're in the right directory
cd kimigpt

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Upgrade pip
python -m pip install --upgrade pip

# 4. Reinstall everything
pip install -r requirements.txt --force-reinstall

# 5. Check Python version
python --version
```

---

## ✅ Checklist Before Asking for Help

- [ ] Python 3.7-3.11 installed
- [ ] Ran `diagnose.py` - all checks pass
- [ ] Virtual environment activated
- [ ] Requirements installed: `pip list | grep flask`
- [ ] .env file exists and has at least ONE API key
- [ ] Firewall allows Python
- [ ] Port 5000 is not used by another app
- [ ] Tried reinstalling from scratch

---

## 📚 Useful Commands

```bash
# Check Python version
python --version

# Check if package is installed
pip list | grep flask

# See what's using port 5000
netstat -ano | findstr :5000

# Test if Flask imports
python -c "import flask; print('Flask OK!')"

# Test if Groq imports
python -c "import groq; print('Groq OK!')"

# Run diagnostics
python diagnose.py

# Start with verbose logging
python src/ui/app.py
```

---

## 🎯 Most Common Fix

**90% of issues are solved by:**
```bash
cd kimigpt
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
notepad .env    # Add your API keys here
startgpt.bat
```

---

## 📖 Additional Resources

- **API Setup Guide:** See `api.txt`
- **Quick Start:** See `QUICKSTART.md`
- **Full Documentation:** See `README.md`
- **System Check:** Run `python diagnose.py`
