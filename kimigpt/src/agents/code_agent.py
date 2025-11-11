"""
KimiGPT - Code Generation Agent
Generates production-ready HTML/CSS/JavaScript code
"""

import logging
from typing import Dict, Any, Optional
import json

logger = logging.getLogger(__name__)


class CodeAgent:
    """
    Code Generation Agent
    - Writes HTML/CSS/JavaScript code
    - Implements requested functionality
    - Follows best practices and clean code principles
    - Optimizes for performance
    - Generates multiple framework versions if needed
    """

    def __init__(self, api_manager):
        """Initialize Code Agent"""
        self.api_manager = api_manager

    def generate_code(self, analysis: Dict[str, Any],
                     page_count: int = 1,
                     task_1_output: Optional[Dict] = None,
                     task_3_output: Optional[Dict] = None,
                     task_4_output: Optional[Dict] = None,
                     **kwargs) -> Dict[str, Any]:
        """
        Generate complete website code

        Args:
            analysis: Website analysis
            page_count: Number of pages to generate
            task_1_output: Requirements from Understanding Agent
            task_3_output: Design from Design Agent
            task_4_output: Content from Content Agent
            **kwargs: Additional context

        Returns:
            Generated website files
        """
        logger.info("Code Agent: Generating website code...")

        requirements = task_1_output or {}
        design = task_3_output or {}
        content = task_4_output or {}

        # Generate HTML
        html_code = self._generate_html(analysis, requirements, design, content)

        # Generate CSS
        css_code = self._generate_css(design, requirements)

        # Generate JavaScript (if needed)
        js_code = ""
        if requirements.get("technical_requirements", {}).get("javascript_needed"):
            js_code = self._generate_javascript(requirements)

        # Package result
        result = {
            "files": {
                "index.html": html_code,
                "css/styles.css": css_code,
                "js/main.js": js_code
            },
            "structure": {
                "pages": page_count,
                "framework": requirements.get("technical_requirements", {}).get("framework", "vanilla")
            }
        }

        logger.info("✓ Code generation completed successfully")

        return result

    def _generate_html(self, analysis: Dict, requirements: Dict,
                      design: Dict, content: Dict) -> str:
        """Generate HTML code"""
        logger.info("Generating HTML...")

        website_type = analysis.get("website_type", "business")
        sections = analysis.get("sections", ["hero", "features", "contact"])

        prompt = f"""Generate professional, semantic, accessible HTML5 code for a {website_type} website.

Requirements:
- Website Type: {website_type}
- Sections: {', '.join(sections)}
- Responsive: Yes
- SEO Optimized: Yes
- Accessibility: WCAG AA compliant

Layout Requirements:
{json.dumps(requirements.get('layout_requirements', {}), indent=2)}

Design System:
- Primary Color: {design.get('colors', {}).get('primary', {}).get('main', '#3B82F6')}
- Font Family: {design.get('typography', {}).get('font_families', {}).get('body', 'Inter')}

Generate COMPLETE, PRODUCTION-READY HTML with:
1. Proper DOCTYPE and meta tags
2. SEO meta tags (title, description, Open Graph)
3. Semantic HTML5 elements
4. ARIA labels for accessibility
5. All sections requested: {', '.join(sections)}
6. Proper structure (header, main, footer)
7. Links to external CSS (css/styles.css) and JS (js/main.js)
8. Responsive images with alt tags
9. Contact forms with proper validation attributes
10. Modern, clean structure

DO NOT include any explanations or markdown. Output ONLY the HTML code."""

        response = self.api_manager.generate(
            prompt,
            preferred_provider="deepseek",
            task_type="code",
            temperature=0.3,
            max_tokens=4000
        )

        if response.get("success"):
            html = response["response"]
            # Clean up any markdown code blocks
            html = html.replace("```html", "").replace("```", "").strip()
            return html
        else:
            logger.warning("Using template HTML")
            return self._get_template_html(website_type, sections)

    def _generate_css(self, design: Dict, requirements: Dict) -> str:
        """Generate CSS code"""
        logger.info("Generating CSS...")

        design_style = requirements.get("design_requirements", {})

        prompt = f"""Generate professional, modern CSS code using this design system:

Design System:
{json.dumps(design, indent=2)}

Generate COMPLETE CSS with:
1. CSS Custom Properties (variables) for design tokens
2. Modern CSS Reset
3. Responsive typography using clamp()
4. Flexbox and CSS Grid layouts
5. Mobile-first responsive design with media queries
6. Smooth animations and transitions
7. Hover effects and interactive states
8. Utility classes for spacing, colors
9. Component styles (buttons, cards, forms)
10. Print styles

Breakpoints:
- Mobile: 375px+
- Tablet: 768px+
- Desktop: 1024px+
- Wide: 1440px+

Requirements:
- Modern, clean aesthetics
- Smooth transitions
- Accessible focus states
- Cross-browser compatible
- Optimized for performance

DO NOT include explanations or markdown. Output ONLY CSS code."""

        response = self.api_manager.generate(
            prompt,
            preferred_provider="deepseek",
            task_type="code",
            temperature=0.3,
            max_tokens=4000
        )

        if response.get("success"):
            css = response["response"]
            css = css.replace("```css", "").replace("```", "").strip()
            return css
        else:
            return self._get_template_css(design)

    def _generate_javascript(self, requirements: Dict) -> str:
        """Generate JavaScript code"""
        logger.info("Generating JavaScript...")

        functional_reqs = requirements.get("functional_requirements", {})

        prompt = f"""Generate modern, vanilla JavaScript (ES6+) for website functionality:

Requirements:
- Forms: {', '.join(functional_reqs.get('forms', []))}
- Interactive Elements: {', '.join(functional_reqs.get('interactive_elements', []))}
- Mobile Menu: Yes
- Smooth Scrolling: Yes
- Form Validation: Yes

Generate COMPLETE JavaScript with:
1. Mobile navigation toggle
2. Smooth scroll for anchor links
3. Form validation and submission
4. Intersection Observer for animations
5. Lazy loading for images
6. Accordion/tabs functionality (if needed)
7. Modal functionality (if needed)
8. Event listeners with proper error handling
9. Performance optimizations
10. No jQuery - vanilla JS only

Code should be:
- Modern ES6+ syntax
- Well-commented
- Performant
- Accessible (keyboard navigation)
- Error-handled

DO NOT include explanations. Output ONLY JavaScript code."""

        response = self.api_manager.generate(
            prompt,
            preferred_provider="deepseek",
            task_type="code",
            temperature=0.3,
            max_tokens=3000
        )

        if response.get("success"):
            js = response["response"]
            js = js.replace("```javascript", "").replace("```js", "").replace("```", "").strip()
            return js
        else:
            return self._get_template_javascript()

    def _get_template_html(self, website_type: str, sections: list) -> str:
        """Get template HTML as fallback"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Professional {website_type} website">
    <title>{website_type.title()} Website | KimiGPT</title>
    <link rel="stylesheet" href="css/styles.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700&display=swap" rel="stylesheet">
</head>
<body>
    <header class="header">
        <div class="container">
            <nav class="nav">
                <div class="logo">Logo</div>
                <ul class="nav-menu">
                    {"".join(f'<li><a href="#{section}">{section.title()}</a></li>' for section in sections)}
                </ul>
                <button class="mobile-toggle" aria-label="Toggle navigation">
                    <span></span><span></span><span></span>
                </button>
            </nav>
        </div>
    </header>

    <main>
        <section id="hero" class="hero">
            <div class="container">
                <h1>Welcome to Your New Website</h1>
                <p>Professional, modern, and responsive design.</p>
                <button class="btn btn-primary">Get Started</button>
            </div>
        </section>

        {''.join(f'''<section id="{section}" class="{section}">
            <div class="container">
                <h2>{section.title()}</h2>
                <p>Content for {section} section.</p>
            </div>
        </section>''' for section in sections if section != 'hero')}
    </main>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2024 Your Company. All rights reserved.</p>
        </div>
    </footer>

    <script src="js/main.js"></script>
</body>
</html>"""

    def _get_template_css(self, design: Dict) -> str:
        """Get template CSS as fallback"""
        primary = design.get("colors", {}).get("primary", {}).get("main", "#3B82F6")
        return f"""/* KimiGPT Generated Styles */

:root {{
  --color-primary: {primary};
  --color-text: #1F2937;
  --color-bg: #FFFFFF;
  --font-family: 'Inter', sans-serif;
  --container-width: 1200px;
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
  font-family: var(--font-family);
  color: var(--color-text);
  line-height: 1.6;
  background: var(--color-bg);
}}

.container {{
  max-width: var(--container-width);
  margin: 0 auto;
  padding: 0 1rem;
}}

.header {{
  padding: 1rem 0;
  border-bottom: 1px solid #e5e7eb;
}}

.nav {{
  display: flex;
  justify-content: space-between;
  align-items: center;
}}

.nav-menu {{
  display: flex;
  gap: 2rem;
  list-style: none;
}}

.hero {{
  padding: 4rem 0;
  text-align: center;
}}

.hero h1 {{
  font-size: clamp(2rem, 5vw, 3.5rem);
  margin-bottom: 1rem;
}}

.btn {{
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
}}

.btn-primary {{
  background: var(--color-primary);
  color: white;
}}

.btn-primary:hover {{
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}}

section {{
  padding: 4rem 0;
}}

.footer {{
  padding: 2rem 0;
  text-align: center;
  background: #f9fafb;
  margin-top: 4rem;
}}

@media (max-width: 768px) {{
  .nav-menu {{ display: none; }}
}}"""

    def _get_template_javascript(self) -> str:
        """Get template JavaScript as fallback"""
        return """// KimiGPT Generated JavaScript

// Mobile Navigation
const mobileToggle = document.querySelector('.mobile-toggle');
const navMenu = document.querySelector('.nav-menu');

if (mobileToggle) {
  mobileToggle.addEventListener('click', () => {
    navMenu.classList.toggle('active');
  });
}

// Smooth Scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

// Form Validation
const forms = document.querySelectorAll('form');
forms.forEach(form => {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    // Add your form handling logic here
    console.log('Form submitted');
  });
});

console.log('Website loaded successfully');"""
