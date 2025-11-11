"""
KimiGPT - Quality Assurance Agent
"""

import logging
from typing import Dict, Any
import re

logger = logging.getLogger(__name__)


class QAAgent:
    """QA Agent - tests and validates generated websites"""

    def __init__(self, api_manager):
        self.api_manager = api_manager

    def test_website(self, requirements: Dict[str, Any],
                    task_5_output: Dict = None,
                    **kwargs) -> Dict[str, Any]:
        """Test and validate website"""
        logger.info("QA Agent: Testing website...")

        files = task_5_output.get("files", {}) if task_5_output else {}

        results = {
            "html_validation": self._validate_html(files.get("index.html", "")),
            "css_validation": self._validate_css(files.get("css/styles.css", "")),
            "accessibility": self._check_accessibility(files.get("index.html", "")),
            "seo": self._check_seo(files.get("index.html", "")),
            "responsive": self._check_responsive(files.get("css/styles.css", "")),
            "performance": self._check_performance(files)
        }

        # Calculate overall score
        scores = [r.get("score", 0) for r in results.values()]
        overall_score = sum(scores) / len(scores) if scores else 0

        results["overall_score"] = overall_score
        results["passed"] = overall_score >= 80

        logger.info(f"✓ QA completed - Score: {overall_score:.1f}/100")

        return results

    def _validate_html(self, html: str) -> Dict:
        """Validate HTML structure"""
        issues = []
        score = 100

        # Check for DOCTYPE
        if not html.startswith("<!DOCTYPE html>"):
            issues.append("Missing DOCTYPE declaration")
            score -= 10

        # Check for meta viewport
        if "viewport" not in html:
            issues.append("Missing viewport meta tag")
            score -= 10

        # Check for semantic tags
        semantic_tags = ["header", "main", "footer", "section", "nav"]
        for tag in semantic_tags:
            if f"<{tag}" not in html:
                score -= 5

        return {"score": max(score, 0), "issues": issues}

    def _validate_css(self, css: str) -> Dict:
        """Validate CSS"""
        issues = []
        score = 100

        # Check for modern CSS features
        if ":root" not in css:
            issues.append("No CSS variables found")
            score -= 10

        if "@media" not in css:
            issues.append("No media queries found")
            score -= 15

        return {"score": max(score, 0), "issues": issues}

    def _check_accessibility(self, html: str) -> Dict:
        """Check accessibility"""
        issues = []
        score = 100

        # Check for alt attributes on images
        img_tags = re.findall(r'<img[^>]*>', html)
        for img in img_tags:
            if 'alt=' not in img:
                issues.append("Image missing alt attribute")
                score -= 5

        # Check for semantic HTML
        if "<h1" not in html:
            issues.append("Missing h1 heading")
            score -= 10

        # Check for aria-label on buttons without text
        buttons = re.findall(r'<button[^>]*>', html)
        for btn in buttons:
            if 'aria-label' not in btn and '>' not in btn:
                score -= 3

        return {"score": max(score, 0), "issues": issues}

    def _check_seo(self, html: str) -> Dict:
        """Check SEO optimization"""
        issues = []
        score = 100

        # Check for title tag
        if "<title>" not in html:
            issues.append("Missing title tag")
            score -= 20

        # Check for meta description
        if 'name="description"' not in html:
            issues.append("Missing meta description")
            score -= 15

        # Check for Open Graph tags
        if 'property="og:' not in html:
            issues.append("Missing Open Graph tags")
            score -= 10

        return {"score": max(score, 0), "issues": issues}

    def _check_responsive(self, css: str) -> Dict:
        """Check responsive design"""
        score = 100
        issues = []

        # Count media queries
        media_query_count = css.count("@media")

        if media_query_count == 0:
            issues.append("No responsive design detected")
            score = 40
        elif media_query_count < 2:
            issues.append("Limited responsive breakpoints")
            score = 70

        return {"score": score, "issues": issues}

    def _check_performance(self, files: Dict) -> Dict:
        """Check performance metrics"""
        score = 100
        issues = []

        # Check file sizes
        html_size = len(files.get("index.html", ""))
        css_size = len(files.get("css/styles.css", ""))
        js_size = len(files.get("js/main.js", ""))

        if html_size > 50000:
            issues.append("HTML file is large")
            score -= 10

        if css_size > 100000:
            issues.append("CSS file is large")
            score -= 10

        return {"score": score, "issues": issues}
