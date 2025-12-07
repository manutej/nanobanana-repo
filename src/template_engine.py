"""
Template Engine - Simple prompt enhancement with domain-specific templates

Takes user input and enhances it with professional photography/diagram/art specifications.
This is just string formatting - no fancy category theory needed!
"""

import json
from pathlib import Path
from typing import Dict, Optional


class TemplateEngine:
    """
    Enhances user prompts using domain-specific templates.

    Example:
        engine = TemplateEngine()
        enhanced = engine.enhance(
            user_input="headshot of CEO",
            domain="photography",
            quality="expert"
        )
        # Returns: "headshot of CEO, award-winning professional corporate portrait,
        #           shot on Phase One XF IQ4 150MP, Schneider Kreuznach 110mm..."
    """

    def __init__(self, templates_path: Optional[str] = None):
        """
        Initialize template engine with templates from JSON file.

        Args:
            templates_path: Path to templates.json file
                           (defaults to ../templates/templates.json)
        """
        if templates_path is None:
            # Default to templates directory
            current_dir = Path(__file__).parent
            templates_path = current_dir.parent / "templates" / "templates.json"

        with open(templates_path, "r") as f:
            self.templates: Dict = json.load(f)

    def enhance(
        self,
        user_input: str,
        domain: str,
        quality: str = "detailed",
        subcategory: Optional[str] = None
    ) -> str:
        """
        Enhance user prompt with domain-specific template.

        Args:
            user_input: User's original prompt (e.g., "headshot of CEO")
            domain: One of ["photography", "diagrams", "art", "products"]
            quality: One of ["basic", "detailed", "expert"] (default: "detailed")
            subcategory: Optional subcategory (e.g., "portrait", "landscape")
                        If None, uses first available subcategory

        Returns:
            Enhanced prompt with professional specifications

        Example:
            enhanced = engine.enhance(
                "sunset over mountains",
                domain="photography",
                quality="expert"
            )
        """
        # Validate domain
        if domain not in self.templates:
            raise ValueError(
                f"Unknown domain: {domain}. "
                f"Must be one of {list(self.templates.keys())}"
            )

        domain_templates = self.templates[domain]

        # Auto-select subcategory if not provided
        if subcategory is None:
            subcategory = list(domain_templates.keys())[0]

        # Validate subcategory
        if subcategory not in domain_templates:
            raise ValueError(
                f"Unknown subcategory '{subcategory}' for domain '{domain}'. "
                f"Available: {list(domain_templates.keys())}"
            )

        # Validate quality
        quality_templates = domain_templates[subcategory]
        if quality not in quality_templates:
            raise ValueError(
                f"Unknown quality: {quality}. "
                f"Must be one of {list(quality_templates.keys())}"
            )

        # Get template
        template = quality_templates[quality]

        # Simple string formatting - replace {subject} with user input
        enhanced = template.replace("{subject}", user_input)

        return enhanced

    def get_available_subcategories(self, domain: str) -> list[str]:
        """
        Get list of available subcategories for a domain.

        Args:
            domain: Domain name

        Returns:
            List of subcategory names

        Example:
            subcats = engine.get_available_subcategories("photography")
            # Returns: ["portrait", "landscape", "product", "macro"]
        """
        if domain not in self.templates:
            return []

        return list(self.templates[domain].keys())

    def suggest_subcategory(self, user_input: str, domain: str) -> str:
        """
        Suggest best subcategory based on user input keywords.

        Args:
            user_input: User's prompt
            domain: Domain name

        Returns:
            Suggested subcategory name

        Example:
            subcat = engine.suggest_subcategory("CEO portrait", "photography")
            # Returns: "portrait"
        """
        if domain not in self.templates:
            return list(self.templates[domain].keys())[0]  # Default to first

        user_input_lower = user_input.lower()
        subcategories = self.get_available_subcategories(domain)

        # Simple keyword matching for subcategories
        subcategory_keywords = {
            "portrait": ["portrait", "headshot", "face", "person", "people"],
            "landscape": ["landscape", "scenery", "mountains", "sunset", "nature"],
            "product": ["product", "item", "package", "merchandise"],
            "macro": ["macro", "close-up", "detail", "extreme"],
            "architecture": ["architecture", "system", "infrastructure", "microservices"],
            "flowchart": ["flow", "process", "workflow", "steps"],
            "wireframe": ["wireframe", "mockup", "UI", "interface", "screen"],
            "technical": ["technical", "schematic", "engineering", "blueprint"],
            "painting": ["painting", "paint", "impressionist", "oil", "watercolor"],
            "digital_art": ["digital", "illustration", "artwork"],
            "3d_render": ["3D", "render", "blender", "cinema 4d"],
            "abstract": ["abstract", "geometric", "shapes"],
            "ecommerce": ["ecommerce", "amazon", "shopify", "store"],
            "lifestyle": ["lifestyle", "real-world", "in use"],
            "editorial": ["editorial", "magazine", "fashion"],
            "advertising": ["advertising", "commercial", "campaign"]
        }

        # Score each subcategory
        scores = {}
        for subcat in subcategories:
            keywords = subcategory_keywords.get(subcat, [])
            score = sum(1 for kw in keywords if kw in user_input_lower)
            scores[subcat] = score

        # Return subcategory with highest score, or first if no matches
        max_score = max(scores.values())
        if max_score == 0:
            return subcategories[0]

        return max(scores, key=scores.get)


# Convenience function for simple usage
def enhance_prompt(
    user_input: str,
    domain: str,
    quality: str = "detailed"
) -> str:
    """
    Quick enhancement function - use this for simple cases.

    Args:
        user_input: User's prompt
        domain: Domain name
        quality: Quality tier

    Returns:
        Enhanced prompt

    Example:
        enhanced = enhance_prompt(
            "headshot of CEO",
            "photography",
            "expert"
        )
    """
    engine = TemplateEngine()
    subcategory = engine.suggest_subcategory(user_input, domain)
    return engine.enhance(user_input, domain, quality, subcategory)


if __name__ == "__main__":
    # Quick test
    engine = TemplateEngine()

    test_cases = [
        ("headshot of a CEO", "photography", "expert"),
        ("AWS architecture diagram", "diagrams", "detailed"),
        ("sunset painting", "art", "basic"),
        ("product photo for Amazon", "products", "detailed")
    ]

    print("Template Enhancement Tests:\n")
    for user_input, domain, quality in test_cases:
        subcategory = engine.suggest_subcategory(user_input, domain)
        enhanced = engine.enhance(user_input, domain, quality, subcategory)

        print(f"Input: {user_input}")
        print(f"Domain: {domain} ({subcategory})")
        print(f"Quality: {quality}")
        print(f"Enhanced: {enhanced[:150]}...\n")
