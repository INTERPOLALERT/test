# 🤖 KimiGPT - Multi-Agent AI Website Builder

> Revolutionary AGI-style system that generates professional, production-ready websites using 8 specialized AI agents with intelligent API rotation across multiple free AI providers.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## 🎯 What is KimiGPT?

KimiGPT is an advanced Multi-Agent AI System that orchestrates 8 specialized AI agents to generate complete, professional websites from ANY input type - text prompts, images, audio, video, or documents. The system features intelligent API rotation across 5+ free AI providers with automatic failover, real-time preview, and one-click deployment.

### ✨ Key Features

- **🤖 8 Specialized AI Agents** - Each agent handles a specific aspect of website creation
- **🔄 Smart API Rotation** - Automatically switches between 5 FREE AI providers for maximum reliability
- **📱 Fully Responsive** - Websites work perfectly on mobile, tablet, and desktop
- **⚡ Production Ready** - SEO optimized, accessible (WCAG AA), and performant code
- **🎨 Multi-Modal Input** - Upload images, videos, audio, documents - we handle it all
- **👁️ Real-Time Preview** - See your website as it's being generated
- **📦 One-Click Deploy** - Download ZIP or deploy to Netlify/Vercel instantly
- **🔒 Secure & Private** - All processing happens locally, your data stays yours

## 🏗️ Multi-Agent Architecture

```
┌─────────────────────────────────────────────────┐
│         MASTER ORCHESTRATOR AGENT               │
│  (Coordinates all agents and manages workflow)  │
└─────────────────┬───────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
┌───────▼────────┐  ┌──────▼───────┐
│ UNDERSTANDING  │  │    DESIGN    │
│     AGENT      │  │     AGENT    │
│  (NLP & Req.)  │  │ (UI/UX, CSS) │
└───────┬────────┘  └──────┬───────┘
        │                   │
        └─────────┬─────────┘
                  │
        ┌─────────▼─────────┐
        │   CODE GENERATION │
        │       AGENT       │
        │  (HTML/CSS/JS)    │
        └─────────┬─────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼────┐  ┌────▼─────┐  ┌───▼────┐
│ IMAGE  │  │ CONTENT  │  │   QA   │
│ AGENT  │  │  AGENT   │  │ AGENT  │
└───┬────┘  └────┬─────┘  └───┬────┘
    │            │            │
    └────────────┼────────────┘
                 │
         ┌───────▼────────┐
         │  DEPLOYMENT    │
         │     AGENT      │
         │ (Package & Deploy)
         └────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Windows 10/11** (or Linux with minor modifications)
- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **At least ONE API key** (see [API Setup](#-api-setup))

### Installation (3 Simple Steps)

1. **Download KimiGPT**
   ```bash
   # Clone or download this repository
   git clone https://github.com/yourusername/kimigpt.git
   cd kimigpt
   ```

2. **Run Installation Wizard**
   ```bash
   # Double-click or run:
   installgpt.bat
   ```

   The installer will:
   - ✓ Check system requirements
   - ✓ Create virtual environment
   - ✓ Install all dependencies
   - ✓ Configure API keys (interactive)
   - ✓ Initialize database
   - ✓ Create desktop shortcut

3. **Launch KimiGPT**
   ```bash
   # Double-click or run:
   startgpt.bat
   ```

   Then open: **http://localhost:5000**

## 🔑 API Setup

KimiGPT requires at least ONE API key to function. All providers offer generous free tiers!

### Quick Setup Guide

1. Get API keys from these providers (see `api.txt` for detailed instructions):

| Provider | Free Tier | Best For | Get Key |
|----------|-----------|----------|---------|
| **Groq** ⭐ | 14,400 req/day | ⚡ Speed (Recommended!) | [console.groq.com](https://console.groq.com/) |
| **Google Gemini** | 60 req/min | 🎨 Multi-modal | [makersuite.google.com](https://makersuite.google.com/app/apikey) |
| **DeepSeek** | Free credits | 💻 Coding | [platform.deepseek.com](https://platform.deepseek.com/) |
| **OpenRouter** | Free models | 🔄 Variety | [openrouter.ai](https://openrouter.ai/keys) |
| **Mistral AI** | €5 credit | 🇪🇺 European | [console.mistral.ai](https://console.mistral.ai/) |

2. Add keys to `.env` file (minimum ONE key required):
   ```env
   GROQ_API_KEY=gsk_your_key_here
   GEMINI_API_KEY=AIzaSy_your_key_here
   DEEPSEEK_API_KEY=sk_your_key_here
   ```

3. The system will automatically use the best available API!

> 💡 **Pro Tip**: Add multiple API keys for maximum reliability and speed!

## 📖 How to Use

### Basic Usage

1. **Open KimiGPT**
   - Run `startgpt.bat`
   - Open http://localhost:5000

2. **Click "Generate Website"**

3. **Describe your website**
   ```
   Example: "Create a modern portfolio website for a photographer
   with dark theme, smooth animations, and a gallery section"
   ```

4. **Upload files (optional)**
   - Images for your website
   - Logo, product photos, etc.
   - Videos to embed
   - Documents to extract content from

5. **Click "Generate"**
   - Watch agents work in real-time
   - Preview updates live
   - Download when ready!

### Advanced Examples

#### Example 1: E-commerce Site
```
Create an e-commerce website for a clothing brand with:
- Hero section with video background
- Product grid with filters
- Shopping cart functionality
- Checkout form
- Dark mode toggle
- Use purple and gold color scheme
```
+ Upload: product images, logo

#### Example 2: Restaurant Website
```
Build a restaurant website with:
- Full-screen image hero
- Menu sections (appetizers, mains, desserts)
- Reservation form
- Google Maps integration
- Gallery of food photos
- Warm, inviting colors
```
+ Upload: food photos, restaurant exterior

#### Example 3: Portfolio
```
Create a minimalist portfolio for a UX designer:
- Animated hero with particles
- Project showcase grid
- About section
- Contact form
- Smooth scroll animations
- Modern, clean aesthetic
```
+ Upload: project screenshots, profile photo

## 🎨 Generated Website Features

Every generated website includes:

### Core Features ✅
- ✓ Fully responsive (mobile, tablet, desktop)
- ✓ Modern HTML5 semantic structure
- ✓ CSS3 with Flexbox and Grid
- ✓ Vanilla JavaScript (no dependencies)
- ✓ Cross-browser compatible
- ✓ Fast loading (< 3 seconds)

### SEO & Accessibility 🌟
- ✓ Meta tags (title, description, Open Graph)
- ✓ Semantic HTML for better SEO
- ✓ WCAG AA compliant
- ✓ ARIA labels for screen readers
- ✓ Alt text for all images
- ✓ Keyboard navigation support

### Performance ⚡
- ✓ Optimized images
- ✓ Minified CSS/JS (optional)
- ✓ Lazy loading
- ✓ Efficient animations
- ✓ No external dependencies (optional)

### Advanced Features (Complexity Dependent) 🚀
- ✓ Smooth scroll animations
- ✓ Intersection Observer effects
- ✓ Dark/Light mode toggle
- ✓ Interactive forms with validation
- ✓ Mobile-friendly navigation
- ✓ Contact form functionality
- ✓ Social media integration
- ✓ Google Maps embed
- ✓ Video backgrounds
- ✓ Image galleries

## 📁 Project Structure

```
kimigpt/
├── src/
│   ├── agents/                   # 🤖 AI Agents
│   │   ├── orchestrator.py      # Master coordinator
│   │   ├── understanding_agent.py
│   │   ├── design_agent.py
│   │   ├── code_agent.py
│   │   ├── image_agent.py
│   │   ├── content_agent.py
│   │   ├── qa_agent.py
│   │   └── deployment_agent.py
│   ├── api/                      # 🔌 API Integrations
│   │   ├── api_manager.py       # Smart rotation
│   │   ├── claude_api.py
│   │   ├── gemini_api.py
│   │   ├── groq_api.py
│   │   ├── deepseek_api.py
│   │   ├── openrouter_api.py
│   │   └── mistral_api.py
│   ├── core/                     # ⚙️ Core Engine
│   │   ├── multi_agent_system.py
│   │   ├── preview_server.py
│   │   └── init_db.py
│   └── ui/                       # 🖥️ Web Interface
│       ├── app.py               # Flask application
│       └── templates/
│           ├── index.html       # Dashboard
│           └── generator.html   # Generator page
├── generated_sites/              # 💾 Your Websites
├── uploads/                      # 📎 User Uploads
├── temp/                         # ⏳ Preview Files
├── database/                     # 💽 SQLite DB
├── installgpt.bat               # 🚀 Installer
├── startgpt.bat                 # ▶️ Launcher
├── requirements.txt              # 📦 Dependencies
├── config.json                   # ⚙️ Configuration
├── .env                          # 🔑 API Keys
├── api.txt                       # 📄 API Guide
└── README.md                     # 📖 This file
```

## 🔧 Configuration

Edit `config.json` to customize:

- **API Priorities**: Change which API is used first
- **Agent Settings**: Configure agent behavior
- **Template Options**: Modify default templates
- **Feature Flags**: Enable/disable features
- **Optimization**: Adjust performance settings

Example:
```json
{
  "api_providers": {
    "groq": {
      "priority": 1,
      "default_model": "llama-3.1-70b-versatile"
    }
  },
  "features": {
    "animations": { "enabled": true },
    "pwa": { "enabled": false }
  }
}
```

## 🐛 Troubleshooting

### Common Issues

**Problem**: "No API providers available"
- **Solution**: Add at least one API key to `.env` file
- See `api.txt` for detailed setup instructions

**Problem**: "Python not found"
- **Solution**: Install Python 3.8+ from python.org
- Make sure to check "Add Python to PATH" during installation

**Problem**: "Module not found"
- **Solution**: Run `installgpt.bat` again or manually:
  ```bash
  pip install -r requirements.txt
  ```

**Problem**: Website generation fails
- **Solution**: Check `logs/app.log` for errors
- Verify API keys are valid
- Try a simpler prompt first

**Problem**: Preview not loading
- **Solution**: Check if port 5000 is available
- Try accessing http://127.0.0.1:5000 instead

### Need More Help?

1. Check `logs/` folder for detailed error logs
2. Review `api.txt` for API setup instructions
3. Verify `.env` file has correct API keys
4. Test APIs using: `python src/api/test_apis.py`

## 📊 System Requirements

### Minimum
- Windows 10 or Linux
- Python 3.8+
- 4GB RAM
- 1GB free disk space
- Internet connection

### Recommended
- Windows 11 or Ubuntu 20.04+
- Python 3.10+
- 8GB RAM
- 5GB free disk space
- Fast internet (for API calls)

## 🔒 Security & Privacy

- ✅ All processing happens locally
- ✅ API keys stored securely in `.env`
- ✅ No telemetry or tracking
- ✅ Generated code is clean and secure
- ✅ Input validation and sanitization
- ✅ No data sent to third parties (except AI APIs)

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙏 Credits

Built with:
- Flask - Web framework
- Google Gemini - Multi-modal AI
- Groq - Ultra-fast inference
- And many more amazing open-source projects

## 🚀 Future Enhancements

- [ ] React/Vue/Next.js code generation
- [ ] Figma design import
- [ ] Direct deployment to hosting
- [ ] Website editing (iterative improvements)
- [ ] Template library
- [ ] Mobile app
- [ ] Collaboration features
- [ ] Version control integration

## 📞 Support

- **Issues**: Open an issue on GitHub
- **Documentation**: Check `docs/` folder
- **API Help**: Read `api.txt`
- **Community**: Join our Discord (coming soon)

---

<div align="center">

**Made with ❤️ by KimiGPT Team**

⭐ Star this repo if you find it useful!

[Report Bug](https://github.com/yourusername/kimigpt/issues) · [Request Feature](https://github.com/yourusername/kimigpt/issues) · [Documentation](https://github.com/yourusername/kimigpt/wiki)

</div>
