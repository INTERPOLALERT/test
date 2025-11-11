"""
KimiGPT - Content Generation Agent
"""

import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class ContentAgent:
    """Content Agent - generates website copy and content"""

    def __init__(self, api_manager):
        self.api_manager = api_manager

    def generate_content(self, analysis: Dict[str, Any],
                        sections: List[str],
                        task_1_output: Dict = None,
                        **kwargs) -> Dict[str, Any]:
        """Generate website content"""
        logger.info("Content Agent: Generating content...")

        website_type = analysis.get("website_type", "business")
        style = analysis.get("design_style", "modern")

        prompt = f"""Generate professional website content for a {website_type} website:

Style: {style}
Sections: {', '.join(sections)}

Generate content in JSON format:
{{
    "hero": {{
        "headline": "Compelling main headline",
        "subheadline": "Supporting text that explains value",
        "cta_text": "Call to action button text"
    }},
    "sections": {{
        "features": {{
            "heading": "Section heading",
            "items": [
                {{"title": "Feature 1", "description": "Description"}},
                {{"title": "Feature 2", "description": "Description"}},
                {{"title": "Feature 3", "description": "Description"}}
            ]
        }},
        "about": {{
            "heading": "About heading",
            "text": "About section content"
        }},
        "contact": {{
            "heading": "Contact heading",
            "text": "Get in touch message"
        }}
    }},
    "meta": {{
        "title": "SEO optimized page title",
        "description": "SEO meta description (150-160 chars)"
    }}
}}

Make content professional, engaging, and SEO-optimized."""

        response = self.api_manager.generate(
            prompt,
            preferred_provider="anthropic",
            task_type="text",
            temperature=0.7
        )

        if response.get("success"):
            import json
            try:
                content_text = response["response"]
                start_idx = content_text.find("{")
                end_idx = content_text.rfind("}") + 1
                content = json.loads(content_text[start_idx:end_idx])
            except:
                content = self._get_default_content(website_type)
        else:
            content = self._get_default_content(website_type)

        logger.info("✓ Content generated successfully")
        return content

    def _get_default_content(self, website_type: str) -> Dict:
        """Get default content"""
        return {
            "hero": {
                "headline": f"Welcome to Our {website_type.title()}",
                "subheadline": "Professional solutions for your needs",
                "cta_text": "Get Started"
            },
            "sections": {
                "features": {
                    "heading": "Our Features",
                    "items": [
                        {"title": "Feature 1", "description": "Description of feature 1"},
                        {"title": "Feature 2", "description": "Description of feature 2"},
                        {"title": "Feature 3", "description": "Description of feature 3"}
                    ]
                }
            },
            "meta": {
                "title": f"{website_type.title()} Website",
                "description": f"Professional {website_type} website with modern design"
            }
        }
