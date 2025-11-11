"""
KimiGPT - Understanding Agent
Processes and understands user requirements through NLP
"""

import logging
from typing import Dict, List, Any, Optional
import json

logger = logging.getLogger(__name__)


class UnderstandingAgent:
    """
    Understanding Agent (Natural Language Processing)
    - Parses user prompts (text, voice commands)
    - Extracts requirements (colors, layout, features, style)
    - Identifies website type
    - Creates structured task list for other agents
    """

    def __init__(self, api_manager):
        """Initialize Understanding Agent"""
        self.api_manager = api_manager

    def process_requirements(self, analysis: Dict[str, Any],
                           attachments: Optional[List[Dict]] = None,
                           **kwargs) -> Dict[str, Any]:
        """
        Process and extract detailed requirements

        Args:
            analysis: Initial analysis from orchestrator
            attachments: User attachments
            **kwargs: Additional context

        Returns:
            Structured requirements document
        """
        logger.info("Understanding Agent: Processing requirements...")

        # Build detailed requirements extraction prompt
        prompt = f"""Based on this website analysis, extract detailed technical requirements:

Website Type: {analysis.get('website_type')}
Complexity: {analysis.get('complexity')}
Style: {analysis.get('design_style')}
Features: {', '.join(analysis.get('key_features', []))}
Sections: {', '.join(analysis.get('sections', []))}

Extract and structure the following requirements in JSON:
{{
    "technical_requirements": {{
        "responsive": true,
        "framework": "vanilla" or "react" or "vue",
        "css_framework": "vanilla" or "tailwind" or "bootstrap",
        "javascript_needed": true/false,
        "animations": true/false,
        "seo_optimization": true/false,
        "accessibility": true/false
    }},
    "layout_requirements": {{
        "header": {{"style": "fixed|static|transparent", "includes": ["logo", "navigation"]}},
        "hero_section": {{"type": "image|video|gradient", "call_to_action": true/false}},
        "content_sections": [
            {{"name": "features", "layout": "grid|list|cards", "columns": 3}},
            {{"name": "about", "layout": "text|two-column"}}
        ],
        "footer": {{"includes": ["social_links", "copyright", "contact"]}}
    }},
    "design_requirements": {{
        "color_scheme": {{
            "primary": "#hexcode",
            "secondary": "#hexcode",
            "accent": "#hexcode",
            "background": "#hexcode",
            "text": "#hexcode"
        }},
        "typography": {{
            "heading_font": "font-name",
            "body_font": "font-name",
            "font_sizes": {{"h1": "size", "body": "size"}}
        }},
        "spacing": {{"padding": "value", "margin": "value"}},
        "border_radius": "value",
        "shadows": true/false
    }},
    "content_requirements": {{
        "hero_headline": "Main headline text or [GENERATE]",
        "hero_subheadline": "Subtext or [GENERATE]",
        "sections_content": {{
            "section_name": "content or [GENERATE]"
        }},
        "call_to_actions": ["CTA text or [GENERATE]"]
    }},
    "functional_requirements": {{
        "forms": ["contact", "newsletter"],
        "interactive_elements": ["accordion", "tabs", "modals"],
        "media": {{"images": true, "video": false, "audio": false}},
        "third_party": {{"google_maps": false, "analytics": true}}
    }}
}}

Provide complete, valid JSON."""

        # Get requirements from API
        response = self.api_manager.generate(
            prompt,
            preferred_provider="gemini",
            task_type="text",
            temperature=0.4
        )

        if not response.get("success"):
            logger.error("Failed to process requirements")
            return self._get_default_requirements(analysis)

        # Parse requirements
        try:
            requirements_text = response["response"]
            # Extract JSON
            start_idx = requirements_text.find("{")
            end_idx = requirements_text.rfind("}") + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = requirements_text[start_idx:end_idx]
                requirements = json.loads(json_str)
            else:
                raise ValueError("No JSON found")

        except Exception as e:
            logger.warning(f"Failed to parse requirements: {e}")
            requirements = self._get_default_requirements(analysis)

        # Enhance requirements with attachment analysis
        if attachments:
            requirements["attachments_analysis"] = self._analyze_attachments(attachments)

        logger.info("✓ Requirements processed successfully")

        return requirements

    def _analyze_attachments(self, attachments: List[Dict]) -> Dict[str, Any]:
        """Analyze uploaded attachments"""
        analysis = {
            "total_count": len(attachments),
            "images": [],
            "videos": [],
            "documents": [],
            "audio": []
        }

        for attachment in attachments:
            file_type = attachment.get("type", "unknown")
            if file_type == "image":
                analysis["images"].append({
                    "name": attachment.get("name"),
                    "size": attachment.get("size"),
                    "usage": "auto-detect"
                })
            elif file_type == "video":
                analysis["videos"].append({
                    "name": attachment.get("name"),
                    "usage": "embed"
                })
            elif file_type == "document":
                analysis["documents"].append({
                    "name": attachment.get("name"),
                    "extract_content": True
                })
            elif file_type == "audio":
                analysis["audio"].append({
                    "name": attachment.get("name"),
                    "transcribe": True
                })

        return analysis

    def _get_default_requirements(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Get default requirements based on website type"""
        website_type = analysis.get("website_type", "business")
        complexity = analysis.get("complexity", "moderate")

        # Default technical requirements
        technical = {
            "responsive": True,
            "framework": "vanilla",
            "css_framework": "vanilla",
            "javascript_needed": complexity in ["moderate", "advanced"],
            "animations": complexity != "simple",
            "seo_optimization": True,
            "accessibility": True
        }

        # Default layout based on website type
        layouts = {
            "portfolio": {
                "header": {"style": "fixed", "includes": ["logo", "navigation"]},
                "hero_section": {"type": "image", "call_to_action": True},
                "content_sections": [
                    {"name": "projects", "layout": "grid", "columns": 3},
                    {"name": "about", "layout": "two-column"},
                    {"name": "contact", "layout": "form"}
                ],
                "footer": {"includes": ["social_links", "copyright"]}
            },
            "business": {
                "header": {"style": "static", "includes": ["logo", "navigation", "cta"]},
                "hero_section": {"type": "gradient", "call_to_action": True},
                "content_sections": [
                    {"name": "features", "layout": "cards", "columns": 3},
                    {"name": "about", "layout": "two-column"},
                    {"name": "testimonials", "layout": "slider"},
                    {"name": "contact", "layout": "form"}
                ],
                "footer": {"includes": ["links", "contact", "social_links", "copyright"]}
            },
            "landing_page": {
                "header": {"style": "transparent", "includes": ["logo", "cta"]},
                "hero_section": {"type": "image", "call_to_action": True},
                "content_sections": [
                    {"name": "benefits", "layout": "list", "columns": 1},
                    {"name": "features", "layout": "grid", "columns": 3},
                    {"name": "cta", "layout": "centered"}
                ],
                "footer": {"includes": ["copyright"]}
            }
        }

        layout = layouts.get(website_type, layouts["business"])

        # Default design
        design = {
            "color_scheme": {
                "primary": "#3B82F6",
                "secondary": "#1E40AF",
                "accent": "#F59E0B",
                "background": "#FFFFFF",
                "text": "#1F2937"
            },
            "typography": {
                "heading_font": "Inter",
                "body_font": "Inter",
                "font_sizes": {"h1": "3rem", "body": "1rem"}
            },
            "spacing": {"padding": "1rem", "margin": "1rem"},
            "border_radius": "0.5rem",
            "shadows": True
        }

        # Default content
        content = {
            "hero_headline": "[GENERATE]",
            "hero_subheadline": "[GENERATE]",
            "sections_content": {},
            "call_to_actions": ["[GENERATE]"]
        }

        # Default functional requirements
        functional = {
            "forms": ["contact"] if website_type != "portfolio" else [],
            "interactive_elements": ["accordion"] if complexity == "advanced" else [],
            "media": {"images": True, "video": False, "audio": False},
            "third_party": {"google_maps": False, "analytics": True}
        }

        return {
            "technical_requirements": technical,
            "layout_requirements": layout,
            "design_requirements": design,
            "content_requirements": content,
            "functional_requirements": functional
        }

    def extract_color_preferences(self, user_input: str) -> List[str]:
        """Extract color preferences from user input"""
        # Simple color extraction (can be enhanced)
        colors = []
        color_words = {
            "blue": "#3B82F6", "red": "#EF4444", "green": "#10B981",
            "yellow": "#F59E0B", "purple": "#8B5CF6", "pink": "#EC4899",
            "orange": "#F97316", "gray": "#6B7280", "black": "#000000",
            "white": "#FFFFFF"
        }

        user_input_lower = user_input.lower()
        for color_name, hex_code in color_words.items():
            if color_name in user_input_lower:
                colors.append(hex_code)

        return colors if colors else ["#3B82F6"]  # Default to blue
