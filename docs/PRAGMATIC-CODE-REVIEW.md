# NanoBanana Pragmatic Code Review

**Date**: 2025-12-07
**Reviewer**: Pragmatic Programmer Agent
**Context**: Preparing codebase for multi-media factory evolution and meta-prompting orchestration

---

## Executive Summary

**Current State**: Clean, working monolith with good separation of concerns
**Code Quality**: 7/10 - Good foundation with some technical debt
**Readiness for Evolution**: 6/10 - Needs refactoring for extensibility

**Top 3 Priorities**:
1. **Extract template data from code** (2 hours) - Blocks rapid iteration
2. **Centralized error handling** (3 hours) - Reduces maintenance burden
3. **Configuration management** (2 hours) - Enables environment-specific settings

---

## 1. Code Smell Detection

### Issue #1: Primitive Obsession in Domain Classification

**Location**: `domain_classifier.py` lines 25-54
**Smell**: Using dictionaries of string lists instead of proper domain types

**What's Wrong**:
```python
DOMAIN_KEYWORDS: Dict[str, List[str]] = {
    "photography": ["photo", "photograph", ...],
    "diagrams": ["diagram", "chart", ...],
    ...
}
```

**Why It Matters**:
- Adding new domains requires code changes
- No validation that domains are consistent
- Hard to add domain-specific behavior (e.g., different confidence thresholds)
- Keyword matching logic is intertwined with domain knowledge

**Pragmatic Fix**:
```python
# domain.py - New file
from dataclasses import dataclass
from typing import List

@dataclass
class Domain:
    name: str
    keywords: List[str]
    confidence_threshold: float = 0.5

    def matches(self, text: str) -> int:
        """Count keyword matches in text."""
        return sum(1 for kw in self.keywords if kw in text.lower())

# Load from YAML config
DOMAINS = [
    Domain("photography", ["photo", "portrait", ...]),
    Domain("diagrams", ["diagram", "chart", ...]),
    ...
]
```

**Effort**: 3 hours
**Priority**: Medium (not blocking, but improves maintainability)

---

### Issue #2: God Object - `main.py` Does Too Much

**Location**: `main.py` - entire file
**Smell**: Flask routes handle orchestration + response formatting + error handling

**What's Wrong**:
- 350+ lines doing routing, orchestration, validation, and HTML generation
- Adding new content types (presentations, UI) requires modifying routes
- Testing requires spinning up Flask server
- Business logic mixed with HTTP concerns

**Why It Matters**:
- Shotgun surgery when adding features
- Can't reuse orchestration logic outside Flask
- Hard to test business logic in isolation

**Pragmatic Fix** (Don't over-engineer):
```python
# service.py - Extract core business logic
class ImageGenerationService:
    """Core business logic - framework agnostic."""

    def __init__(self, classifier, template_engine, gemini_client_factory):
        self.classifier = classifier
        self.template_engine = template_engine
        self.gemini_client_factory = gemini_client_factory

    async def generate_image(
        self,
        prompt: str,
        quality: str = "detailed",
        model: str = "flash"
    ) -> dict:
        """Generate image - returns structured data, not HTTP response."""
        # Step 1: Classify
        domain, confidence = self.classifier.classify_with_confidence(prompt)

        # Step 2: Suggest subcategory
        subcategory = self.template_engine.suggest_subcategory(prompt, domain)

        # Step 3: Enhance
        enhanced = self.template_engine.enhance(
            prompt, domain, quality, subcategory
        )

        # Step 4: Generate
        async with self.gemini_client_factory() as client:
            result = await client.generate_image(enhanced, model=model)

        return {
            "image_data": result["image_data"],
            "mime_type": result["mime_type"],
            "enhanced_prompt": enhanced,
            "domain": domain,
            "subcategory": subcategory,
            "confidence": confidence,
            "model": model
        }

# main.py - Just HTTP adapter
@app.route("/generate", methods=["POST"])
def generate_image():
    data = request.get_json()

    # Validate (extract to validator)
    validation_error = validate_generate_request(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    # Run service
    result = run_async(service.generate_image(
        prompt=data["prompt"],
        quality=data.get("quality", "detailed"),
        model=data.get("model", "flash")
    ))

    # Format response (extract to formatter)
    return format_image_response(result), 200
```

**Effort**: 4 hours
**Priority**: High - Enables testing and reuse

---

### Issue #3: Data Clumps - (domain, subcategory, quality) Passed Together

**Location**: Multiple functions in `template_engine.py` and `main.py`

**What's Wrong**:
```python
# These 3 parameters always travel together
enhance(user_input, domain="photography", quality="detailed", subcategory="portrait")
suggest_subcategory(user_input, domain)
classify_with_confidence(user_input)
```

**Why It Matters**:
- Repetitive parameter passing
- Easy to pass wrong combination
- Adding new parameters (e.g., `style_level`) requires updating all call sites

**Pragmatic Fix**:
```python
from dataclasses import dataclass

@dataclass
class EnhancementRequest:
    """Request for prompt enhancement."""
    user_input: str
    domain: str = None  # Auto-detected if None
    subcategory: str = None  # Auto-suggested if None
    quality: str = "detailed"

    def validate(self):
        """Validate request."""
        if self.quality not in ["basic", "detailed", "expert"]:
            raise ValueError(f"Invalid quality: {self.quality}")

# Usage
request = EnhancementRequest(
    user_input="headshot of CEO",
    quality="expert"
)
enhanced = template_engine.enhance(request)
```

**Effort**: 2 hours
**Priority**: Low (nice to have, but not critical)

---

## 2. DRY Violations (Don't Repeat Yourself)

### Violation #1: Duplicate Keyword Matching Logic

**Location**:
- `domain_classifier.py` lines 74-78 (domain classification)
- `template_engine.py` lines 167-172 (subcategory suggestion)

**Repeated Pattern**:
```python
# domain_classifier.py
scores = {}
for domain, keywords in self.DOMAIN_KEYWORDS.items():
    score = sum(1 for keyword in keywords if keyword in user_input_lower)
    scores[domain] = score

# template_engine.py (nearly identical)
scores = {}
for subcat in subcategories:
    keywords = subcategory_keywords.get(subcat, [])
    score = sum(1 for kw in keywords if kw in user_input_lower)
    scores[subcat] = score
```

**This is TRUE DRY violation** - same **knowledge** (how to score keyword matches) in two places.

**Pragmatic Fix**:
```python
# keyword_matcher.py - Extract shared knowledge
class KeywordMatcher:
    """Shared keyword matching logic."""

    @staticmethod
    def score_matches(
        text: str,
        categories: Dict[str, List[str]]
    ) -> Dict[str, int]:
        """
        Score keyword matches for categories.

        Returns dict mapping category -> match count.
        """
        text_lower = text.lower()
        return {
            category: sum(1 for kw in keywords if kw in text_lower)
            for category, keywords in categories.items()
        }

    @staticmethod
    def best_match(scores: Dict[str, int], default: str = None) -> str:
        """Return category with highest score."""
        max_score = max(scores.values(), default=0)
        if max_score == 0:
            return default
        return max(scores, key=scores.get)

# domain_classifier.py - Use shared logic
scores = KeywordMatcher.score_matches(user_input, self.DOMAIN_KEYWORDS)
best_domain = KeywordMatcher.best_match(scores, default="photography")
```

**Effort**: 1.5 hours
**Priority**: Medium (Rule of Three satisfied - 2 occurrences, close to threshold)

---

### Violation #2: Error Handling Boilerplate

**Location**: All Flask routes (`main.py`)

**Repeated Pattern**:
```python
try:
    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "Missing 'prompt' in request"}), 400
    # ... business logic ...
except ValueError as e:
    return jsonify({"error": str(e)}), 400
except Exception as e:
    print(f"ERROR: {e}")
    return jsonify({"error": "Internal server error", "details": str(e)}), 500
```

**This is TRUE DRY violation** - error handling **knowledge** repeated 4 times.

**Pragmatic Fix**:
```python
# error_handler.py
from functools import wraps
from flask import jsonify
import logging

logger = logging.getLogger(__name__)

def handle_api_errors(f):
    """Decorator for consistent error handling."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"Validation error: {e}")
            return jsonify({"error": str(e)}), 400
        except httpx.HTTPError as e:
            logger.error(f"External API error: {e}")
            return jsonify({
                "error": "External service error",
                "details": str(e)
            }), 502
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            return jsonify({
                "error": "Internal server error",
                "details": str(e) if app.debug else "Contact support"
            }), 500
    return decorated_function

# Usage
@app.route("/generate", methods=["POST"])
@handle_api_errors
def generate_image():
    # Clean business logic - no try/except needed
    data = require_json_field(request, "prompt")
    ...
```

**Effort**: 2 hours
**Priority**: High - Reduces maintenance, improves logging

---

### Violation #3: Response Formatting Duplication

**Location**: `main.py` - all routes return similar JSON structure

**Not a Real DRY Violation** (only 2 occurrences, violates Rule of Three)

**Pragmatic Decision**: Wait for 3rd occurrence before abstracting.

---

## 3. SOLID Principles Assessment

### Single Responsibility Principle (SRP)

**Violations**:

1. **`domain_classifier.py` - Mixed Responsibilities** ✅ Actually OK
   - Classification logic ✓
   - Confidence calculation ✓
   - Score debugging ✓
   - **Verdict**: Single responsibility (domain classification). Different methods, same purpose.

2. **`template_engine.py` - Two Responsibilities** ⚠️
   - Template enhancement (lines 44-105)
   - Subcategory suggestion (lines 126-179)
   - **Verdict**: Borderline. Subcategory suggestion could be separate, but tightly coupled to templates.

3. **`main.py` - Four Responsibilities** ❌
   - HTTP routing
   - Request validation
   - Orchestration
   - Response formatting
   - **Verdict**: Clear violation (see Issue #2)

**Pragmatic Fix**: Extract service layer (already covered in Issue #2)

---

### Open/Closed Principle (OCP)

**Question**: Can we add new content types (presentations, UI, videos) without modifying existing code?

**Current State**: ❌ No

**Why**:
- Adding "presentations" domain requires:
  - Modifying `DOMAIN_KEYWORDS` dict in `domain_classifier.py`
  - Adding templates to `templates.json`
  - No code change needed in `template_engine.py` ✓ (good!)
  - No code change needed in `main.py` ✓ (good!)

**Partially Open**: Template engine is extensible via config, but classifier isn't.

**Pragmatic Fix**:
```python
# domains.yaml - External configuration
domains:
  - name: photography
    keywords: [photo, portrait, headshot, ...]
    confidence_threshold: 0.5

  - name: diagrams
    keywords: [diagram, chart, flowchart, ...]
    confidence_threshold: 0.6

  - name: presentations
    keywords: [slide, deck, powerpoint, keynote, ...]
    confidence_threshold: 0.5

# domain_classifier.py - Load from config
class DomainClassifier:
    def __init__(self, config_path="config/domains.yaml"):
        with open(config_path) as f:
            domains = yaml.safe_load(f)["domains"]
        self.DOMAIN_KEYWORDS = {
            d["name"]: d["keywords"] for d in domains
        }
```

**Effort**: 2 hours
**Priority**: High - Critical for evolution to multi-media factory

---

### Dependency Inversion Principle (DIP)

**Question**: Do high-level modules depend on abstractions or concrete implementations?

**Current State**: Mixed

**Good**:
```python
# main.py - Depends on concrete classes directly
classifier = DomainClassifier()  # Concrete
template_engine = TemplateEngine()  # Concrete
```

**Problem**:
- Hard to test with mocks
- Can't swap implementations (e.g., LLM-based classifier vs keyword-based)

**Pragmatic Fix** (only where it helps testing):
```python
# classifier_interface.py
from abc import ABC, abstractmethod

class ClassifierInterface(ABC):
    @abstractmethod
    def classify_with_confidence(self, text: str) -> Tuple[str, float]:
        pass

# Concrete implementations
class KeywordClassifier(ClassifierInterface):
    """Keyword-based classification (current)."""
    ...

class LLMClassifier(ClassifierInterface):
    """LLM-based classification (future)."""
    ...

# main.py - Depend on abstraction
def create_app(classifier: ClassifierInterface = None):
    if classifier is None:
        classifier = KeywordClassifier()  # Default

    service = ImageGenerationService(
        classifier=classifier,
        template_engine=template_engine
    )
    ...
```

**Effort**: 3 hours
**Priority**: Medium - Helps with testing and future LLM integration

---

## 4. Refactoring Opportunities

### Opportunity #1: Extract Method - Long `generate_image()` Route

**Location**: `main.py` lines 55-165 (110 lines)

**Extract**:
```python
def validate_generate_request(data: dict) -> Optional[str]:
    """Validate generate request. Returns error message or None."""
    if not data or "prompt" not in data:
        return "Missing 'prompt' in request"

    quality = data.get("quality", "detailed")
    if quality not in ["basic", "detailed", "expert"]:
        return f"Invalid quality: {quality}. Must be basic/detailed/expert"

    model = data.get("model", "flash")
    if model not in ["flash", "pro"]:
        return f"Invalid model: {model}. Must be flash/pro"

    return None

def format_base64_response(result: dict, metadata: dict) -> dict:
    """Format image result as base64 response."""
    image_b64 = base64.b64encode(result["image_data"]).decode("utf-8")
    return {
        "image": f"data:{result['mime_type']};base64,{image_b64}",
        "enhanced_prompt": metadata["enhanced_prompt"],
        "domain": metadata["domain"],
        "subcategory": metadata["subcategory"],
        "model": metadata["model"],
        "metadata": {
            "original_prompt": metadata["original_prompt"],
            "quality": metadata["quality"],
            "domain_confidence": metadata["confidence"],
            "image_size_bytes": len(result["image_data"]),
            "mime_type": result["mime_type"],
            "timestamp": datetime.utcnow().isoformat()
        }
    }
```

**Effort**: 1 hour
**Priority**: Low (doesn't block features, just readability)

---

### Opportunity #2: Extract Class - Subcategory Suggester

**Location**: `template_engine.py` lines 126-179

**Current**: `suggest_subcategory()` method with hard-coded keywords

**Refactor**:
```python
# subcategory_suggester.py
class SubcategorySuggester:
    """Suggests subcategories based on keywords."""

    def __init__(self, keywords_path="config/subcategory_keywords.yaml"):
        with open(keywords_path) as f:
            self.keywords = yaml.safe_load(f)

    def suggest(self, text: str, available_subcategories: List[str]) -> str:
        """Suggest best subcategory from available options."""
        scores = KeywordMatcher.score_matches(text, self.keywords)

        # Filter to only available subcategories
        filtered_scores = {
            k: v for k, v in scores.items()
            if k in available_subcategories
        }

        return KeywordMatcher.best_match(
            filtered_scores,
            default=available_subcategories[0]
        )
```

**Effort**: 2 hours
**Priority**: Medium - Enables configuration-driven subcategories

---

### Opportunity #3: Introduce Parameter Object

**Covered in Issue #3 (Data Clumps)**

---

### Opportunity #4: Replace Magic Strings with Constants

**Location**: Multiple files

**Magic Strings**:
```python
"photography", "diagrams", "art", "products"  # Domains
"basic", "detailed", "expert"  # Quality levels
"flash", "pro"  # Models
```

**Pragmatic Fix**:
```python
# constants.py
from enum import Enum

class Domain(str, Enum):
    PHOTOGRAPHY = "photography"
    DIAGRAMS = "diagrams"
    ART = "art"
    PRODUCTS = "products"

class Quality(str, Enum):
    BASIC = "basic"
    DETAILED = "detailed"
    EXPERT = "expert"

class Model(str, Enum):
    FLASH = "flash"
    PRO = "pro"

# Usage
if domain not in [d.value for d in Domain]:
    raise ValueError(f"Invalid domain: {domain}")
```

**Effort**: 1 hour
**Priority**: Low (nice to have, prevents typos)

---

## 5. Error Handling & Logging

### Current State: Ad-hoc and Inconsistent

**Issues**:
1. ❌ Print statements instead of logging (`gemini_client.py` line 151, `main.py` line 160)
2. ❌ Generic exception handling loses error context
3. ❌ No structured logging (can't query logs)
4. ❌ No error recovery strategies (retry, fallback, circuit breaker)
5. ✓ Good: Retry logic in `gemini_client.py` (lines 102-153)

**Pragmatic Improvements**:

```python
# logging_config.py
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    """Format logs as JSON for structured logging."""

    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)

def setup_logging(level=logging.INFO):
    """Configure structured logging."""
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())

    logging.basicConfig(
        level=level,
        handlers=[handler]
    )

# gemini_client.py - Replace print with logging
logger = logging.getLogger(__name__)

# Line 151: Replace print
logger.warning(
    "API call failed",
    extra={
        "attempt": attempt + 1,
        "max_retries": max_retries,
        "error": str(e)
    }
)
```

**Circuit Breaker Pattern** (for external API resilience):
```python
# circuit_breaker.py
from datetime import datetime, timedelta

class CircuitBreaker:
    """Prevent cascading failures to external APIs."""

    def __init__(self, failure_threshold=5, timeout_seconds=60):
        self.failure_threshold = failure_threshold
        self.timeout = timedelta(seconds=timeout_seconds)
        self.failures = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open

    def call(self, func, *args, **kwargs):
        if self.state == "open":
            if datetime.now() - self.last_failure_time > self.timeout:
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise

    def on_success(self):
        self.failures = 0
        self.state = "closed"

    def on_failure(self):
        self.failures += 1
        self.last_failure_time = datetime.now()

        if self.failures >= self.failure_threshold:
            self.state = "open"

# Usage in gemini_client.py
circuit_breaker = CircuitBreaker()

async def generate_image(self, prompt, model="flash"):
    return await circuit_breaker.call(
        self._generate_image_impl,
        prompt,
        model
    )
```

**Effort**: 4 hours
**Priority**: High - Production-critical for reliability

---

## 6. Testing Strategy

### Current State: No Tests Visible ❌

**Pragmatic Testing Approach** (for monolith):

**Don't write**: 100+ unit tests covering every function
**Do write**: 5-10 integration tests covering critical paths

**Critical Paths**:
1. Happy path: User prompt → Enhanced prompt → Image generation
2. Domain classification accuracy
3. Error handling (missing API key, invalid model, API failure)
4. Retry logic works
5. Template enhancement works

**Pragmatic Test Suite**:
```python
# tests/test_critical_paths.py
import pytest
from unittest.mock import Mock, patch
import asyncio

# Test 1: Happy path
@pytest.mark.asyncio
async def test_generate_image_happy_path():
    """End-to-end: prompt → classification → enhancement → generation."""

    from src.domain_classifier import DomainClassifier
    from src.template_engine import TemplateEngine
    from src.gemini_client import GeminiClient

    classifier = DomainClassifier()
    template_engine = TemplateEngine()

    # Mock GeminiClient to avoid real API calls
    with patch.object(GeminiClient, 'generate_image') as mock_gen:
        mock_gen.return_value = {
            "image_data": b"fake_image_data",
            "mime_type": "image/png",
            "model": "flash",
            "prompt": "enhanced prompt"
        }

        # Simulate full flow
        user_prompt = "professional headshot of CEO"
        domain, confidence = classifier.classify_with_confidence(user_prompt)

        assert domain == "photography"
        assert confidence > 0.5

        subcategory = template_engine.suggest_subcategory(user_prompt, domain)
        enhanced = template_engine.enhance(user_prompt, domain, "detailed", subcategory)

        assert "Canon EOS R5" in enhanced or "professional" in enhanced.lower()

        async with GeminiClient() as client:
            result = await client.generate_image(enhanced)

        assert result["image_data"] == b"fake_image_data"

# Test 2: Domain classification accuracy
@pytest.mark.parametrize("prompt,expected_domain", [
    ("headshot of CEO", "photography"),
    ("AWS architecture diagram", "diagrams"),
    ("impressionist painting of garden", "art"),
    ("product photo for Amazon", "products"),
])
def test_domain_classification(prompt, expected_domain):
    """Verify classifier accuracy on known inputs."""
    from src.domain_classifier import DomainClassifier

    classifier = DomainClassifier()
    domain, confidence = classifier.classify_with_confidence(prompt)

    assert domain == expected_domain
    assert confidence > 0.5

# Test 3: API error handling
@pytest.mark.asyncio
async def test_gemini_client_retry_on_failure():
    """Verify retry logic with exponential backoff."""
    from src.gemini_client import GeminiClient
    import httpx

    with patch('httpx.AsyncClient.post') as mock_post:
        # Simulate 2 failures, then success
        mock_post.side_effect = [
            httpx.HTTPError("Timeout"),
            httpx.HTTPError("Timeout"),
            Mock(
                status_code=200,
                json=lambda: {
                    "candidates": [{
                        "content": {
                            "parts": [{
                                "inlineData": {
                                    "data": "base64data",
                                    "mimeType": "image/png"
                                }
                            }]
                        }
                    }]
                }
            )
        ]

        async with GeminiClient() as client:
            result = await client.generate_image("test prompt", max_retries=3)

        assert result["image_data"] is not None
        assert mock_post.call_count == 3  # 2 failures + 1 success

# Test 4: Missing API key
def test_gemini_client_requires_api_key():
    """Verify API key validation."""
    from src.gemini_client import GeminiClient
    import os

    # Clear API key
    old_key = os.environ.get("GOOGLE_API_KEY")
    if old_key:
        del os.environ["GOOGLE_API_KEY"]

    try:
        with pytest.raises(ValueError, match="API key required"):
            client = GeminiClient(api_key=None)
    finally:
        if old_key:
            os.environ["GOOGLE_API_KEY"] = old_key

# Test 5: Template enhancement
def test_template_enhancement():
    """Verify templates enhance prompts correctly."""
    from src.template_engine import TemplateEngine

    engine = TemplateEngine()

    enhanced = engine.enhance(
        "sunset over mountains",
        domain="photography",
        quality="expert"
    )

    # Should contain photography specs
    assert any(x in enhanced for x in ["Sony", "Canon", "ISO", "f/"])
    assert len(enhanced) > 100  # Detailed enhancement
```

**Run Tests**:
```bash
pip install pytest pytest-asyncio
pytest tests/test_critical_paths.py -v
```

**Coverage Goal**: 80% of critical paths, not 100% line coverage

**Effort**: 6 hours
**Priority**: High - Prevents regressions

---

## 7. Configuration Management

### Current State: Mixed (Good and Bad)

**Good**:
- ✓ API keys from environment variables (`gemini_client.py` line 42)
- ✓ Templates in external JSON (`templates.json`)

**Bad**:
- ❌ Domain keywords hard-coded in Python
- ❌ Subcategory keywords hard-coded in Python
- ❌ No dev/staging/prod configs
- ❌ No configuration validation

**Pragmatic Fix**:

```yaml
# config/domains.yaml
domains:
  photography:
    keywords: [photo, portrait, headshot, camera, lens, ...]
    confidence_threshold: 0.5
  diagrams:
    keywords: [diagram, chart, flowchart, AWS, architecture, ...]
    confidence_threshold: 0.6
  art:
    keywords: [art, painting, illustration, watercolor, ...]
    confidence_threshold: 0.5
  products:
    keywords: [product, ecommerce, catalog, Amazon, ...]
    confidence_threshold: 0.5

# config/subcategories.yaml
subcategories:
  portrait: [portrait, headshot, face, person, people]
  landscape: [landscape, scenery, mountains, sunset, nature]
  product: [product, item, package, merchandise]
  macro: [macro, close-up, detail, extreme]
  # ... more

# config/settings.py
from dataclasses import dataclass
import os
import yaml

@dataclass
class Settings:
    """Application settings."""

    # API Configuration
    google_api_key: str
    default_model: str = "flash"
    default_quality: str = "detailed"

    # Paths
    templates_path: str = "templates/templates.json"
    domains_config: str = "config/domains.yaml"
    subcategories_config: str = "config/subcategories.yaml"

    # Timeouts
    api_timeout: float = 30.0
    max_retries: int = 3

    # Logging
    log_level: str = "INFO"

    @classmethod
    def from_env(cls, env: str = "production"):
        """Load settings from environment."""
        return cls(
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            default_model=os.getenv("DEFAULT_MODEL", "flash"),
            log_level=os.getenv("LOG_LEVEL", "INFO")
        )

    def validate(self):
        """Validate settings."""
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable required")

        if self.default_model not in ["flash", "pro"]:
            raise ValueError(f"Invalid default_model: {self.default_model}")

# main.py - Use settings
settings = Settings.from_env()
settings.validate()

classifier = DomainClassifier(config_path=settings.domains_config)
template_engine = TemplateEngine(templates_path=settings.templates_path)
```

**Environment-Specific Configs**:
```bash
# .env.development
GOOGLE_API_KEY=dev_key_here
DEFAULT_MODEL=flash
LOG_LEVEL=DEBUG

# .env.production
GOOGLE_API_KEY=prod_key_here
DEFAULT_MODEL=flash
LOG_LEVEL=WARNING
```

**Effort**: 3 hours
**Priority**: High - Enables environment-specific behavior

---

## 8. Meta-Prompting Preparation

### Goal: Prepare for Recursive Prompt Improvement

**Current State**: `llm_prompt_enhancer.py` exists but not integrated

**Design Questions**:

1. **Integration**: Separate module or integrated?
   - **Answer**: Separate module that can be **optionally** enabled
   - **Reason**: Keep keyword-based classifier as fast fallback

2. **Infinite Loop Prevention**: How to avoid recursive meta-prompting?
   - **Answer**: Max depth limit (2-3 levels)
   - **Implementation**:
   ```python
   async def meta_enhance(prompt: str, depth: int = 0, max_depth: int = 2):
       if depth >= max_depth:
           return prompt  # Stop recursion

       enhanced = await llm_enhancer.enhance_prompt(prompt)

       # Quality check: Is enhancement better?
       quality_score = await evaluate_quality(enhanced["enhanced_prompt"])

       if quality_score > QUALITY_THRESHOLD:
           return enhanced["enhanced_prompt"]
       else:
           # Try meta-prompting the meta-prompt
           return await meta_enhance(enhanced["enhanced_prompt"], depth + 1, max_depth)
   ```

3. **When to Stop Refining**: Quality threshold or max iterations?
   - **Answer**: Both (whichever comes first)
   - **Quality Metrics**:
     - Prompt length (100-300 words ideal)
     - Specificity score (count of technical terms)
     - Confidence score from LLM

4. **Which Model**: Claude API or Gemini?
   - **Pragmatic Answer**: Use Gemini (already integrated)
   - **Future**: Abstract to support both

5. **Cost Control**: LLM calls are expensive
   - **Solution**: Cache enhancements by (prompt, quality, domain)
   - **Implementation**:
   ```python
   from functools import lru_cache
   import hashlib

   @lru_cache(maxsize=1000)
   def get_cached_enhancement(prompt_hash: str, domain: str, quality: str):
       # Check cache
       pass

   async def enhance_with_cache(prompt: str, domain: str, quality: str):
       prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
       cached = get_cached_enhancement(prompt_hash, domain, quality)

       if cached:
           return cached

       enhanced = await llm_enhancer.enhance_prompt(prompt)
       get_cached_enhancement.cache_info()  # Monitor hit rate
       return enhanced
   ```

**Pragmatic Meta-Prompting Architecture**:
```python
# meta_prompter.py
class MetaPrompter:
    """Intelligent meta-prompting with quality gates."""

    def __init__(
        self,
        enhancer: LLMPromptEnhancer,
        max_depth: int = 2,
        quality_threshold: float = 0.8,
        cache_size: int = 1000
    ):
        self.enhancer = enhancer
        self.max_depth = max_depth
        self.quality_threshold = quality_threshold
        self.cache = {}  # Simple in-memory cache

    async def enhance(
        self,
        prompt: str,
        depth: int = 0
    ) -> Dict:
        """
        Recursively enhance prompt until quality threshold met.

        Returns:
            - final_prompt: str
            - iterations: int
            - quality_score: float
            - enhancement_path: List[str] (for debugging)
        """
        # Check cache
        cache_key = f"{prompt}:{depth}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Base case: max depth reached
        if depth >= self.max_depth:
            return {
                "final_prompt": prompt,
                "iterations": depth,
                "quality_score": await self._evaluate_quality(prompt),
                "enhancement_path": [prompt],
                "stopped_reason": "max_depth"
            }

        # Enhance prompt
        enhanced = await self.enhancer.enhance_prompt(prompt)
        quality = await self._evaluate_quality(enhanced["enhanced_prompt"])

        # Quality gate: Good enough?
        if quality >= self.quality_threshold:
            result = {
                "final_prompt": enhanced["enhanced_prompt"],
                "iterations": depth + 1,
                "quality_score": quality,
                "enhancement_path": [prompt, enhanced["enhanced_prompt"]],
                "stopped_reason": "quality_threshold"
            }
            self.cache[cache_key] = result
            return result

        # Recurse: Try to improve further
        result = await self.enhance(enhanced["enhanced_prompt"], depth + 1)
        result["enhancement_path"].insert(0, prompt)
        return result

    async def _evaluate_quality(self, prompt: str) -> float:
        """
        Evaluate prompt quality (0.0-1.0).

        Metrics:
        - Length (100-300 words ideal)
        - Specificity (count technical terms)
        - Coherence (no contradictions)
        """
        words = prompt.split()
        word_count = len(words)

        # Length score
        if 100 <= word_count <= 300:
            length_score = 1.0
        elif word_count < 50:
            length_score = 0.5
        else:
            length_score = 0.8  # Too long but okay

        # Specificity score (simple heuristic)
        technical_terms = [
            "ISO", "f/", "mm", "Canon", "Sony", "Nikon",
            "architecture", "flowchart", "UML", "AWS",
            "impressionist", "oil painting", "brushstrokes"
        ]
        specificity_score = min(
            sum(1 for term in technical_terms if term in prompt) / 5.0,
            1.0
        )

        # Combined score
        return (length_score * 0.4) + (specificity_score * 0.6)
```

**Integration Point**:
```python
# main.py - Optional meta-prompting
@app.route("/generate", methods=["POST"])
async def generate_image():
    data = request.get_json()
    use_meta_prompting = data.get("meta_prompting", False)

    if use_meta_prompting:
        async with MetaPrompter(LLMPromptEnhancer()) as meta:
            result = await meta.enhance(data["prompt"])
            enhanced_prompt = result["final_prompt"]
    else:
        # Traditional keyword-based enhancement
        domain, _ = classifier.classify_with_confidence(data["prompt"])
        subcategory = template_engine.suggest_subcategory(data["prompt"], domain)
        enhanced_prompt = template_engine.enhance(
            data["prompt"], domain, data.get("quality", "detailed"), subcategory
        )

    # Generate image with enhanced prompt
    ...
```

**Effort**: 8 hours (full meta-prompting system)
**Priority**: Medium - Future feature, not blocking current work

---

## 9. Summary of Prioritized Issues

### High Priority (Do Now) - 17 hours total

| Issue | Description | Effort | Impact |
|-------|-------------|--------|--------|
| Issue #2 | Extract service layer from Flask routes | 4 hours | Enables testing, reuse |
| Violation #2 | Centralized error handling decorator | 2 hours | Reduces maintenance |
| Section 5 | Structured logging + circuit breaker | 4 hours | Production reliability |
| Section 6 | Write 5-10 integration tests | 6 hours | Prevents regressions |
| Section 7 | Configuration management (YAML configs) | 3 hours | Environment flexibility |
| OCP Fix | External domain configuration | 2 hours | Enables new content types |

### Medium Priority (Next Sprint) - 13.5 hours total

| Issue | Description | Effort | Impact |
|-------|-------------|--------|--------|
| Issue #1 | Extract Domain dataclass | 3 hours | Maintainability |
| Violation #1 | Shared keyword matcher | 1.5 hours | DRY compliance |
| Opportunity #2 | Extract SubcategorySuggester | 2 hours | Configuration-driven |
| DIP Fix | Classifier interface for testing | 3 hours | Testability |
| Section 8 | Meta-prompting integration (basic) | 8 hours | Future-proofing |

### Low Priority (Nice to Have) - 4 hours total

| Issue | Description | Effort | Impact |
|-------|-------------|--------|--------|
| Issue #3 | Parameter object for requests | 2 hours | Cleaner API |
| Opportunity #1 | Extract validation methods | 1 hour | Readability |
| Opportunity #4 | Magic strings → Enums | 1 hour | Type safety |

---

## 10. Evolution Roadmap: Monolith → Multi-Media Factory

### Phase 1: Stabilize Foundation (Weeks 1-2)
**Goal**: Production-ready monolith with tests and configs

- ✅ Centralized error handling
- ✅ Structured logging
- ✅ Configuration management
- ✅ Integration tests
- ✅ External domain configs

**Deliverable**: Deployable, testable, maintainable service

### Phase 2: Extract Core Abstractions (Weeks 3-4)
**Goal**: Prepare for multi-content support

- ✅ Service layer extraction
- ✅ Classifier interface
- ✅ Template engine interface
- ✅ Content type abstraction:
  ```python
  class ContentType(ABC):
      @abstractmethod
      def classify(self, prompt: str) -> str:
          pass

      @abstractmethod
      def enhance(self, prompt: str, quality: str) -> str:
          pass

      @abstractmethod
      async def generate(self, enhanced_prompt: str) -> bytes:
          pass

  # Implementations
  class ImageContent(ContentType):  # Current
      ...

  class PresentationContent(ContentType):  # New
      def generate(self, enhanced_prompt: str) -> bytes:
          # Call presentation API
          ...

  class UIComponentContent(ContentType):  # New
      ...
  ```

**Deliverable**: Pluggable content type system

### Phase 3: Add New Content Types (Weeks 5-8)
**Goal**: Multi-media factory

- ✅ Presentations (PowerPoint/Keynote via API)
- ✅ UI Components (Figma/Sketch via API)
- ✅ Diagrams (Excalidraw/Mermaid integration)
- ✅ Videos (text-to-video APIs)

**Deliverable**: Multi-media generation platform

### Phase 4: Meta-Prompting Intelligence (Weeks 9-12)
**Goal**: Recursive prompt optimization

- ✅ LLM-based prompt enhancement
- ✅ Quality evaluation metrics
- ✅ Meta-prompting orchestration
- ✅ Caching and cost optimization
- ✅ A/B testing (template vs LLM enhancement)

**Deliverable**: Intelligent, self-improving prompt system

---

## 11. Pragmatic Recommendations Summary

### Must Do (Before Production)
1. **Centralized error handling** - Prevents debugging nightmares
2. **Structured logging** - Enables observability
3. **Configuration management** - Supports dev/staging/prod
4. **Integration tests** - Catches regressions
5. **Circuit breaker** - Prevents cascade failures

### Should Do (Next 2 Weeks)
1. **Extract service layer** - Enables reuse and testing
2. **External domain configs** - Unblocks new content types
3. **Shared keyword matcher** - Fixes DRY violation
4. **Classifier interface** - Prepares for LLM classifier

### Nice to Have (When Time Permits)
1. **Parameter objects** - Cleaner API
2. **Domain dataclasses** - Better type safety
3. **Enum constants** - Prevents typos

---

## 12. Meta-Analysis: Code Quality Trajectory

### Current State (7/10)
**Strengths**:
- ✅ Clean separation of concerns (classifier, templates, client)
- ✅ Good docstrings and comments
- ✅ Working retry logic
- ✅ Async/await done correctly
- ✅ Pragmatic simplicity (no over-engineering)

**Weaknesses**:
- ❌ Hard-coded configurations
- ❌ No tests
- ❌ Ad-hoc error handling
- ❌ Print instead of logging
- ❌ God object (main.py)

### After High-Priority Fixes (9/10)
**Improvements**:
- ✅ Testable, maintainable codebase
- ✅ Observable via structured logs
- ✅ Resilient to external failures
- ✅ Configurable for multiple environments
- ✅ Ready for new content types

**Remaining Gaps**:
- ⚠️ Limited test coverage (only critical paths)
- ⚠️ Still some hard-coded logic

### After All Fixes (10/10)
**Achieved**:
- ✅ Comprehensive test coverage
- ✅ Fully configuration-driven
- ✅ Pluggable architecture
- ✅ Intelligent meta-prompting
- ✅ Production-grade reliability

---

## 13. Final Pragmatic Advice

### For a Working Developer

**Start Small**:
- Don't try to fix everything at once
- Pick 1-2 high-priority items per week
- Ship working code, iterate

**Validate Impact**:
- Before refactoring, ask: "Does this solve a real problem?"
- Prioritize issues causing actual pain (bugs, slow development, maintenance burden)
- Skip issues that are "theoretically better" but don't help users

**Test Ruthlessly**:
- Tests are your safety net for refactoring
- Write tests for critical paths first
- Don't aim for 100% coverage - aim for confidence

**Keep It Simple**:
- Resist the urge to over-engineer
- YAGNI (You Aren't Gonna Need It) applies to abstractions too
- Add complexity only when proven necessary

**Measure Progress**:
- Track: time to add new feature, deployment frequency, bug rate
- If refactoring doesn't improve these metrics, stop

**Remember**:
> "Good enough for now, easy to improve later" - The Pragmatic Programmer

---

## Appendix A: Quick Wins (1-Hour Tasks)

These can be done individually, incrementally:

1. **Replace print with logging** (30 min)
   - `gemini_client.py` line 151
   - `main.py` line 160

2. **Add type hints** (1 hour)
   - Helps IDEs catch errors early

3. **Extract validation functions** (45 min)
   - `validate_generate_request()`
   - `validate_model()`
   - `validate_quality()`

4. **Add `.env.example` file** (15 min)
   - Helps new developers set up

5. **Write `CONTRIBUTING.md`** (30 min)
   - How to run tests, how to add new domain

---

## Appendix B: Files to Create

Recommended file structure after refactoring:

```
nanobanana-repo/
├── config/
│   ├── domains.yaml              # Domain keywords
│   ├── subcategories.yaml        # Subcategory keywords
│   ├── settings.py               # Settings dataclass
│   └── logging_config.py         # Logging setup
├── src/
│   ├── core/
│   │   ├── classifier_interface.py
│   │   ├── keyword_classifier.py
│   │   ├── llm_classifier.py
│   │   ├── template_engine.py
│   │   └── keyword_matcher.py
│   ├── services/
│   │   ├── image_service.py      # Business logic
│   │   └── meta_prompter.py      # Meta-prompting
│   ├── adapters/
│   │   ├── gemini_client.py
│   │   └── circuit_breaker.py
│   ├── api/
│   │   ├── routes.py             # Flask routes
│   │   ├── validators.py         # Request validation
│   │   ├── formatters.py         # Response formatting
│   │   └── error_handler.py      # Error decorator
│   └── main.py                   # App entry point
├── templates/
│   └── templates.json
├── tests/
│   ├── test_critical_paths.py
│   ├── test_classifiers.py
│   └── test_template_engine.py
└── requirements.txt
```

---

**End of Pragmatic Code Review**

*Generated with care for a working developer who values shipping over perfection.*
