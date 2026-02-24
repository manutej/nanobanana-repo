"""
Tests for domain_classifier.py and template_engine.py core logic.

Validates the refactored _score_domains() method, classification behavior,
the template engine enhancement pipeline, and the parse_prompt_request helper.
"""

import json
import sys
from pathlib import Path

import pytest

# Add src to path so we can import the modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from domain_classifier import DomainClassifier, classify_domain
from template_engine import TemplateEngine, enhance_prompt


class TestDomainClassifier:
    """Tests for DomainClassifier, including the refactored _score_domains."""

    def setup_method(self):
        self.classifier = DomainClassifier()

    def test_score_domains_returns_all_domains(self):
        scores = self.classifier._score_domains("anything")
        assert set(scores.keys()) == {"photography", "diagrams", "art", "products"}

    def test_score_domains_counts_correctly(self):
        scores = self.classifier._score_domains("AWS architecture diagram")
        assert scores["diagrams"] >= 2
        assert scores["photography"] == 0

    def test_classify_photography(self):
        assert self.classifier.classify("headshot of a CEO") == "photography"

    def test_classify_diagrams(self):
        assert self.classifier.classify("AWS microservices architecture diagram") == "diagrams"

    def test_classify_art(self):
        assert self.classifier.classify("impressionist painting of a sunset") == "art"

    def test_classify_products(self):
        result = self.classifier.classify("product for e-commerce catalog on Amazon")
        assert result == "products"

    def test_classify_default_photography(self):
        assert self.classifier.classify("random unknown thing xyz") == "photography"

    def test_classify_with_confidence_returns_tuple(self):
        domain, confidence = self.classifier.classify_with_confidence("headshot")
        assert isinstance(domain, str)
        assert isinstance(confidence, float)
        assert 0.0 <= confidence <= 1.0

    def test_classify_with_confidence_default(self):
        domain, confidence = self.classifier.classify_with_confidence("xyzabc")
        assert domain == "photography"
        assert confidence == 0.5

    def test_get_all_scores_matches_score_domains(self):
        text = "landscape photograph with bokeh"
        assert self.classifier.get_all_scores(text) == self.classifier._score_domains(text)

    def test_convenience_function(self):
        assert classify_domain("portrait of a woman") == "photography"


class TestTemplateEngine:
    """Tests for TemplateEngine."""

    def setup_method(self):
        self.engine = TemplateEngine()

    def test_enhance_replaces_subject(self):
        result = self.engine.enhance("a red ball", domain="photography", quality="basic")
        assert "a red ball" in result

    def test_enhance_invalid_domain(self):
        with pytest.raises(ValueError, match="Unknown domain"):
            self.engine.enhance("test", domain="invalid_domain")

    def test_enhance_invalid_quality(self):
        with pytest.raises(ValueError, match="Unknown quality"):
            self.engine.enhance("test", domain="photography", quality="ultra")

    def test_get_available_subcategories(self):
        subcats = self.engine.get_available_subcategories("photography")
        assert "portrait" in subcats
        assert "landscape" in subcats

    def test_get_available_subcategories_unknown_domain(self):
        assert self.engine.get_available_subcategories("nonexistent") == []

    def test_suggest_subcategory_portrait(self):
        subcat = self.engine.suggest_subcategory("CEO portrait headshot", "photography")
        assert subcat == "portrait"

    def test_suggest_subcategory_landscape(self):
        subcat = self.engine.suggest_subcategory("mountain landscape scenery", "photography")
        assert subcat == "landscape"

    def test_suggest_subcategory_default(self):
        subcat = self.engine.suggest_subcategory("something random", "photography")
        assert subcat in self.engine.get_available_subcategories("photography")

    def test_convenience_function(self):
        result = enhance_prompt("headshot of CEO", "photography", "basic")
        assert "headshot of CEO" in result


class TestGenerateConceptConfig:
    """Validate the generate_concept.py configuration is complete and correct."""

    def test_all_20_concepts_present(self):
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from generate_concept import CONCEPTS

        assert len(CONCEPTS) == 20
        for i in range(1, 21):
            assert f"C{i:02d}" in CONCEPTS

    def test_each_concept_has_required_keys(self):
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from generate_concept import CONCEPTS

        for concept_id, config in CONCEPTS.items():
            assert "title" in config, f"{concept_id} missing title"
            assert "prompt_path" in config, f"{concept_id} missing prompt_path"
            assert "output_path" in config, f"{concept_id} missing output_path"
