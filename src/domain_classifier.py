"""
Domain Classification - Simple keyword matching

Classifies user prompts into one of four domains:
- photography (portraits, landscapes, product photos)
- diagrams (architecture, flowcharts, wireframes)
- art (paintings, illustrations, digital art)
- products (e-commerce, catalog shots)
"""

from typing import Dict, List


class DomainClassifier:
    """
    Classifies user input into image generation domains using keyword matching.

    Example:
        classifier = DomainClassifier()
        domain = classifier.classify("headshot of a CEO")
        # Returns: "photography"
    """

    # Domain keywords - simple and effective
    DOMAIN_KEYWORDS: Dict[str, List[str]] = {
        "photography": [
            "photo", "photograph", "portrait", "headshot", "selfie",
            "picture", "shot", "camera", "lens", "lighting",
            "bokeh", "focus", "exposure", "ISO", "aperture",
            "landscape", "cityscape", "sunset", "golden hour",
            "Canon", "Nikon", "Sony", "Phase One"
        ],
        "diagrams": [
            "diagram", "chart", "graph", "flowchart", "wireframe",
            "architecture", "schematic", "blueprint", "layout",
            "infographic", "visualization", "flow", "process",
            "UML", "ERD", "sequence", "component", "network",
            "AWS", "GCP", "Azure", "microservices", "infrastructure"
        ],
        "art": [
            "art", "artwork", "painting", "drawing", "illustration",
            "sketch", "watercolor", "oil painting", "acrylic",
            "impressionist", "abstract", "surreal", "realistic",
            "digital art", "concept art", "character design",
            "style of", "inspired by", "artistic", "creative"
        ],
        "products": [
            "product", "e-commerce", "catalog", "merchandise",
            "item", "package", "packaging", "unboxing",
            "advertising", "commercial", "marketing", "promotional",
            "studio shot", "white background", "lifestyle",
            "Amazon", "Shopify", "store", "retail"
        ]
    }

    def _score_domains(self, user_input: str) -> Dict[str, int]:
        """Score all domains by counting keyword matches against user input."""
        user_input_lower = user_input.lower()
        return {
            domain: sum(1 for kw in keywords if kw in user_input_lower)
            for domain, keywords in self.DOMAIN_KEYWORDS.items()
        }

    def classify(self, user_input: str) -> str:
        """
        Classify user input into a domain based on keyword matching.

        Args:
            user_input: The user's prompt (e.g., "headshot of CEO")

        Returns:
            Domain name: "photography", "diagrams", "art", or "products"

        Algorithm:
            1. Convert input to lowercase
            2. Count keyword matches for each domain
            3. Return domain with most matches
            4. Default to "photography" if no matches
        """
        scores = self._score_domains(user_input)

        if max(scores.values()) == 0:
            return "photography"

        return max(scores, key=scores.get)

    def classify_with_confidence(self, user_input: str) -> tuple[str, float]:
        """
        Classify with confidence score.

        Args:
            user_input: The user's prompt

        Returns:
            (domain, confidence) where confidence is 0.0-1.0

        Example:
            domain, confidence = classifier.classify_with_confidence("AWS architecture diagram")
            # Returns: ("diagrams", 0.8)
        """
        scores = self._score_domains(user_input)
        total_matches = sum(scores.values())

        if total_matches == 0:
            return "photography", 0.5  # Default with low confidence

        best_domain = max(scores, key=scores.get)
        confidence = scores[best_domain] / total_matches

        return best_domain, confidence

    def get_all_scores(self, user_input: str) -> Dict[str, int]:
        """
        Get keyword match scores for all domains (useful for debugging).

        Args:
            user_input: The user's prompt

        Returns:
            Dictionary mapping domain -> match count

        Example:
            scores = classifier.get_all_scores("architecture diagram")
            # Returns: {"photography": 0, "diagrams": 2, "art": 0, "products": 0}
        """
        return self._score_domains(user_input)


# Convenience function for simple usage
def classify_domain(user_input: str) -> str:
    """
    Quick classification function - use this for simple cases.

    Args:
        user_input: User's prompt

    Returns:
        Domain name

    Example:
        domain = classify_domain("portrait of a woman")
        # Returns: "photography"
    """
    classifier = DomainClassifier()
    return classifier.classify(user_input)


if __name__ == "__main__":
    # Quick test
    classifier = DomainClassifier()

    test_inputs = [
        "headshot of a CEO",
        "AWS microservices architecture diagram",
        "impressionist painting of a sunset",
        "product photography for e-commerce"
    ]

    print("Domain Classification Tests:\n")
    for test_input in test_inputs:
        domain, confidence = classifier.classify_with_confidence(test_input)
        scores = classifier.get_all_scores(test_input)
        print(f"Input: {test_input}")
        print(f"Domain: {domain} (confidence: {confidence:.2f})")
        print(f"Scores: {scores}\n")
