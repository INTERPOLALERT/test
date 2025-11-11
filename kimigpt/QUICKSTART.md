# ⚡ KimiGPT Quick Start Guide

Get started with KimiGPT in under 5 minutes!

## 🚀 Installation (2 minutes)

### Step 1: Get Python
```
📥 Download Python 3.8+: https://www.python.org/downloads/
✅ During install: Check "Add Python to PATH"
```

### Step 2: Install KimiGPT
```batch
1. Extract KimiGPT to a folder (e.g., C:\kimigpt)
2. Double-click: installgpt.bat
3. Wait for installation to complete
```

### Step 3: Get API Keys (1 minute)
Choose ONE (or more) of these FREE options:

#### Option A: Groq (Fastest & Easiest) ⚡
```
1. Go to: https://console.groq.com/
2. Sign up (30 seconds)
3. Create API Key
4. Copy key starting with "gsk_"
```

#### Option B: Google Gemini (Great for Images) 🎨
```
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Create API Key
4. Copy key starting with "AIzaSy"
```

#### Option C: Hugging Face (Unlimited Free) 🌐
```
1. Go to: https://huggingface.co/settings/tokens
2. Sign up (100% FREE - no credit card!)
3. Click "New token"
4. Copy key starting with "hf_"
```

#### Option D: Cohere (Free Tier) 📝
```
1. Go to: https://dashboard.cohere.com/api-keys
2. Sign up (100% FREE - no credit card!)
3. Copy the API key
4. Paste in KimiGPT
```

### Step 4: Configure
When prompted during installation:
```
Enter your API key when asked
OR
Edit .env file and add: GROQ_API_KEY=your_key_here
```

## 🎨 First Website (1 minute)

### Step 1: Launch
```batch
Double-click: startgpt.bat
Wait for browser to open
```

### Step 2: Generate
```
1. Click "Generate Website"
2. Type: "Create a modern portfolio website"
3. Click "Generate Website"
4. Wait 20-30 seconds
5. Preview appears!
6. Click "Download ZIP"
```

### Step 3: Deploy (Optional)
```
📁 Extract ZIP file
🌐 Open index.html in browser
🚀 Upload to Netlify/Vercel for free hosting
```

## 💡 Example Prompts

### Personal Portfolio
```
Create a minimalist portfolio website for a photographer with:
- Dark theme
- Image gallery
- About section
- Contact form
```

### Business Website
```
Build a professional business website with:
- Hero section with company logo
- Services grid (3 columns)
- Testimonials slider
- Contact form
- Modern blue color scheme
```

### Landing Page
```
Create a SaaS landing page with:
- Animated hero section
- Feature highlights
- Pricing table (3 tiers)
- Call-to-action buttons
- Gradient background
```

## 🆘 Quick Troubleshooting

### Problem: "No API providers available"
**Solution**: Add API key to .env file
```
1. Open .env with Notepad
2. Add: GROQ_API_KEY=gsk_your_key_here
3. Save and restart
```

### Problem: Python not found
**Solution**: Reinstall Python
```
1. Uninstall Python
2. Reinstall from python.org
3. ✅ Check "Add Python to PATH"
4. Run installgpt.bat again
```

### Problem: Generation fails
**Solution**: Check API key
```
1. Open .env file
2. Verify API key is correct (no spaces)
3. Test: python src/api/test_apis.py
```

## 📚 Next Steps

- ✅ Read full [README.md](README.md)
- ✅ Check [api.txt](api.txt) for more API providers
- ✅ Experiment with different prompts
- ✅ Upload images for custom designs
- ✅ Try advanced features

## 🎯 Pro Tips

1. **Better Results**: Be specific in prompts
   - ❌ "Make a website"
   - ✅ "Create a modern portfolio with dark theme and animations"

2. **Multiple APIs**: Add 2-3 API keys for reliability
   - System auto-switches if one fails
   - Maximizes free tier usage

3. **Upload Images**: Include your logo/photos
   - System extracts colors
   - Places images intelligently

4. **Edit Generated Code**: All code is clean and readable
   - Easy to customize
   - No obfuscation

## 🚀 You're Ready!

Start creating amazing websites with AI!

---

**Need Help?**
- Read: [README.md](README.md)
- Check: [api.txt](api.txt)
- Issues: GitHub Issues

**Questions?**
Open an issue on GitHub or check the documentation.
