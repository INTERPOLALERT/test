"""
KimiGPT - Design Agent
Creates UI/UX designs, color schemes, and layouts
"""

import logging
from typing import Dict, Any, Optional
import json

logger = logging.getLogger(__name__)


class DesignAgent:
    """
    Design Agent
    - Generates color schemes, typography, layouts
    - Creates responsive design specifications
    - Analyzes reference images for design inspiration
    - Ensures modern UI/UX best practices
    - Produces design tokens (colors, spacing, fonts)
    """

    def __init__(self, api_manager):
        """Initialize Design Agent"""
        self.api_manager = api_manager

    def create_design(self, analysis: Dict[str, Any],
                     has_images: bool = False,
                     task_1_output: Optional[Dict] = None,
                     **kwargs) -> Dict[str, Any]:
        """
        Create complete design system

        Args:
            analysis: Website analysis
            has_images: Whether user uploaded images
            task_1_output: Requirements from Understanding Agent
            **kwargs: Additional context

        Returns:
            Complete design system
        """
        logger.info("Design Agent: Creating design system...")

        requirements = task_1_output or {}

        # Get design preferences from requirements
        design_reqs = requirements.get("design_requirements", {})
        layout_reqs = requirements.get("layout_requirements", {})

        # Generate design system prompt
        prompt = f"""Create a comprehensive design system for a {analysis.get('website_type')} website:

Style: {analysis.get('design_style')}
Complexity: {analysis.get('complexity')}
User Preferences: {json.dumps(design_reqs)}

Generate a complete design system in JSON:
{{
    "colors": {{
        "primary": {{"main": "#hex", "light": "#hex", "dark": "#hex"}},
        "secondary": {{"main": "#hex", "light": "#hex", "dark": "#hex"}},
        "accent": "#hex",
        "backgrounds": {{"main": "#hex", "alt": "#hex"}},
        "text": {{"primary": "#hex", "secondary": "#hex"}},
        "borders": "#hex",
        "success": "#hex",
        "warning": "#hex",
        "error": "#hex"
    }},
    "typography": {{
        "font_families": {{"heading": "Font Name", "body": "Font Name"}},
        "font_sizes": {{
            "h1": "clamp(2rem, 5vw, 3.5rem)",
            "h2": "clamp(1.5rem, 4vw, 2.5rem)",
            "h3": "1.75rem",
            "body": "1rem",
            "small": "0.875rem"
        }},
        "font_weights": {{"light": 300, "normal": 400, "medium": 500, "bold": 700}},
        "line_heights": {{"tight": 1.2, "normal": 1.5, "relaxed": 1.8}}
    }},
    "spacing": {{
        "unit": "8px",
        "scale": {{"xs": "0.5rem", "sm": "1rem", "md": "1.5rem", "lg": "2rem", "xl": "3rem", "2xl": "4rem"}}
    }},
    "layout": {{
        "container_max_width": "1200px",
        "grid_columns": 12,
        "breakpoints": {{"mobile": "375px", "tablet": "768px", "desktop": "1024px", "wide": "1440px"}}
    }},
    "effects": {{
        "border_radius": {{"sm": "0.25rem", "md": "0.5rem", "lg": "1rem", "full": "9999px"}},
        "shadows": {{
            "sm": "0 1px 3px rgba(0,0,0,0.12)",
            "md": "0 4px 6px rgba(0,0,0,0.1)",
            "lg": "0 10px 15px rgba(0,0,0,0.1)"
        }},
        "transitions": {{"fast": "0.15s", "normal": "0.3s", "slow": "0.5s"}}
    }},
    "components": {{
        "button": {{"padding": "0.75rem 1.5rem", "radius": "0.5rem", "font_size": "1rem"}},
        "input": {{"padding": "0.75rem", "radius": "0.5rem", "border": "1px solid"}},
        "card": {{"padding": "1.5rem", "radius": "1rem", "shadow": "md"}}
    }}
}}

Create modern, accessible, professional design. Use complementary colors."""

        # Get design from API
        response = self.api_manager.generate(
            prompt,
            preferred_provider="anthropic",
            task_type="text",
            temperature=0.6
        )

        if not response.get("success"):
            logger.warning("Using default design system")
            return self._get_default_design(analysis)

        # Parse design system
        try:
            design_text = response["response"]
            start_idx = design_text.find("{")
            end_idx = design_text.rfind("}") + 1
            if start_idx >= 0:
                design_system = json.loads(design_text[start_idx:end_idx])
            else:
                raise ValueError("No JSON found")

        except Exception as e:
            logger.warning(f"Failed to parse design: {e}")
            design_system = self._get_default_design(analysis)

        # Generate CSS variables
        design_system["css_variables"] = self._generate_css_variables(design_system)

        logger.info("✓ Design system created successfully")

        return design_system

    def _generate_css_variables(self, design: Dict[str, Any]) -> str:
        """Generate CSS custom properties from design system"""
        css = ":root {\n"

        # Colors
        colors = design.get("colors", {})
        if "primary" in colors:
            css += f"  --color-primary: {colors['primary'].get('main', '#3B82F6')};\n"
        if "secondary" in colors:
            css += f"  --color-secondary: {colors['secondary'].get('main', '#1E40AF')};\n"
        if "accent" in colors:
            css += f"  --color-accent: {colors.get('accent', '#F59E0B')};\n"

        # Typography
        typography = design.get("typography", {})
        if "font_families" in typography:
            fonts = typography["font_families"]
            css += f"  --font-heading: {fonts.get('heading', 'Inter')}, sans-serif;\n"
            css += f"  --font-body: {fonts.get('body', 'Inter')}, sans-serif;\n"

        # Spacing
        spacing = design.get("spacing", {})
        if "scale" in spacing:
            for size, value in spacing["scale"].items():
                css += f"  --space-{size}: {value};\n"

        css += "}\n"

        return css

    def _get_default_design(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Get default design system"""
        return {
            "colors": {
                "primary": {"main": "#3B82F6", "light": "#60A5FA", "dark": "#2563EB"},
                "secondary": {"main": "#1E40AF", "light": "#3B82F6", "dark": "#1E3A8A"},
                "accent": "#F59E0B",
                "backgrounds": {"main": "#FFFFFF", "alt": "#F9FAFB"},
                "text": {"primary": "#1F2937", "secondary": "#6B7280"},
                "borders": "#E5E7EB",
                "success": "#10B981",
                "warning": "#F59E0B",
                "error": "#EF4444"
            },
            "typography": {
                "font_families": {"heading": "Inter", "body": "Inter"},
                "font_sizes": {
                    "h1": "clamp(2rem, 5vw, 3.5rem)",
                    "h2": "clamp(1.5rem, 4vw, 2.5rem)",
                    "h3": "1.75rem",
                    "body": "1rem",
                    "small": "0.875rem"
                },
                "font_weights": {"light": 300, "normal": 400, "medium": 500, "bold": 700},
                "line_heights": {"tight": 1.2, "normal": 1.5, "relaxed": 1.8}
            },
            "spacing": {
                "unit": "8px",
                "scale": {"xs": "0.5rem", "sm": "1rem", "md": "1.5rem", "lg": "2rem", "xl": "3rem"}
            },
            "layout": {
                "container_max_width": "1200px",
                "grid_columns": 12,
                "breakpoints": {"mobile": "375px", "tablet": "768px", "desktop": "1024px"}
            },
            "effects": {
                "border_radius": {"sm": "0.25rem", "md": "0.5rem", "lg": "1rem"},
                "shadows": {
                    "sm": "0 1px 3px rgba(0,0,0,0.12)",
                    "md": "0 4px 6px rgba(0,0,0,0.1)",
                    "lg": "0 10px 15px rgba(0,0,0,0.1)"
                },
                "transitions": {"fast": "0.15s", "normal": "0.3s", "slow": "0.5s"}
            }
        }
