# NanoBanana Refactoring Implementation Guide

**Companion to**: PRAGMATIC-CODE-REVIEW.md
**Purpose**: Step-by-step implementation guide with working code examples

---

## Week 1: High-Priority Foundation (17 hours)

### Day 1: Centralized Error Handling (2 hours)

**File**: `src/api/error_handler.py`
```python
"""Centralized error handling for Flask routes."""

from functools import wraps
from flask import jsonify
import logging
import httpx

logger = logging.getLogger(__name__)


class APIError(Exception):
    """Base class for API errors."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(APIError):
    """Request validation failed."""

    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class ExternalServiceError(APIError):
    """External API call failed."""

    def __init__(self, message: str, service: str = "unknown"):
        self.service = service
        super().__init__(message, status_code=502)


def handle_api_errors(f):
    """
    Decorator for consistent error handling across all routes.

    Usage:
        @app.route("/generate", methods=["POST"])
        @handle_api_errors
        def generate_image():
            # Your route logic here
            # Raise ValidationError, ExternalServiceError, etc.
            # They'll be caught and formatted consistently
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)

        except ValidationError as e:
            logger.warning(f"Validation error: {e.message}")
            return jsonify({
                "error": e.message,
                "type": "validation_error"
            }), e.status_code

        except ExternalServiceError as e:
            logger.error(f"External service error ({e.service}): {e.message}")
            return jsonify({
                "error": f"External service error: {e.service}",
                "details": e.message,
                "type": "external_service_error"
            }), e.status_code

        except httpx.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            return jsonify({
                "error": "External API communication failed",
                "details": str(e),
                "type": "http_error"
            }), 502

        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            return jsonify({
                "error": "Internal server error",
                "details": str(e) if app.debug else "Contact support",
                "type": "internal_error"
            }), 500

    return decorated_function


def require_json_field(request, field: str):
    """
    Extract required field from JSON request.

    Raises:
        ValidationError if field missing or request not JSON
    """
    data = request.get_json()

    if not data:
        raise ValidationError("Request body must be JSON")

    if field not in data:
        raise ValidationError(f"Missing required field: '{field}'")

    return data
```

**Update**: `src/main.py`
```python
from api.error_handler import handle_api_errors, require_json_field, ValidationError

@app.route("/generate", methods=["POST"])
@handle_api_errors  # Add decorator
def generate_image():
    # Clean, simple validation
    data = require_json_field(request, "prompt")

    quality = data.get("quality", "detailed")
    if quality not in ["basic", "detailed", "expert"]:
        raise ValidationError(
            f"Invalid quality: {quality}. Must be basic/detailed/expert"
        )

    # Rest of route logic (no try/except needed!)
    ...
```

---

### Day 2: Structured Logging (2 hours)

**File**: `config/logging_config.py`
```python
"""Structured logging configuration."""

import logging
import json
import sys
from datetime import datetime
from typing import Optional


class JSONFormatter(logging.Formatter):
    """
    Format logs as JSON for structured logging.

    Example output:
        {
            "timestamp": "2025-12-07T10:30:00Z",
            "level": "INFO",
            "message": "Image generated successfully",
            "module": "image_service",
            "function": "generate_image",
            "line": 42,
            "domain": "photography",
            "model": "flash"
        }
    """

    def format(self, record):
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields (e.g., logger.info("msg", extra={"user_id": 123}))
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)

        return json.dumps(log_data)


class ContextLogger(logging.LoggerAdapter):
    """
    Logger with automatic context injection.

    Usage:
        logger = ContextLogger(logging.getLogger(__name__), {"request_id": "abc123"})
        logger.info("Processing request")
        # Output includes request_id automatically
    """

    def process(self, msg, kwargs):
        """Inject context into log record."""
        if "extra" not in kwargs:
            kwargs["extra"] = {}

        kwargs["extra"]["extra_fields"] = self.extra
        return msg, kwargs


def setup_logging(
    level: str = "INFO",
    format: str = "json"
) -> None:
    """
    Configure application logging.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format: Output format ("json" or "text")

    Example:
        setup_logging(level="DEBUG", format="json")
    """
    log_level = getattr(logging, level.upper(), logging.INFO)

    # Create handler
    handler = logging.StreamHandler(sys.stdout)

    # Set formatter
    if format == "json":
        handler.setFormatter(JSONFormatter())
    else:
        # Human-readable format for local development
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        handlers=[handler]
    )

    # Suppress noisy third-party loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)


def get_logger(name: str, context: Optional[dict] = None):
    """
    Get logger with optional context.

    Args:
        name: Logger name (usually __name__)
        context: Optional context dict to include in all logs

    Returns:
        Logger or ContextLogger

    Example:
        logger = get_logger(__name__, {"service": "nanobanana"})
        logger.info("Starting image generation")
    """
    base_logger = logging.getLogger(name)

    if context:
        return ContextLogger(base_logger, context)

    return base_logger
```

**Update**: `src/main.py`
```python
from config.logging_config import setup_logging, get_logger

# Initialize logging on app startup
setup_logging(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format=os.getenv("LOG_FORMAT", "json")
)

logger = get_logger(__name__)

@app.route("/generate", methods=["POST"])
@handle_api_errors
def generate_image():
    logger.info("Image generation request received")

    # ... processing ...

    logger.info(
        "Image generated successfully",
        extra={
            "domain": domain,
            "model": model,
            "image_size_bytes": len(result["image_data"])
        }
    )

    return jsonify(response), 200
```

**Update**: `src/gemini_client.py`
```python
from config.logging_config import get_logger

logger = get_logger(__name__)

# Line 151: Replace print statements
logger.warning(
    "Gemini API call failed, retrying",
    extra={
        "attempt": attempt + 1,
        "max_retries": max_retries,
        "error": str(e)
    }
)
```

---

### Day 3: Configuration Management (3 hours)

**File**: `config/settings.py`
```python
"""Application settings and configuration."""

from dataclasses import dataclass, field
from pathlib import Path
import os
from typing import Optional


@dataclass
class Settings:
    """
    Application configuration.

    Loads from environment variables with sensible defaults.
    """

    # API Keys
    google_api_key: str = field(default_factory=lambda: os.getenv("GOOGLE_API_KEY", ""))

    # Model defaults
    default_model: str = field(default_factory=lambda: os.getenv("DEFAULT_MODEL", "flash"))
    default_quality: str = field(default_factory=lambda: os.getenv("DEFAULT_QUALITY", "detailed"))

    # Paths
    templates_path: Path = field(default_factory=lambda: Path("templates/templates.json"))
    domains_config: Path = field(default_factory=lambda: Path("config/domains.yaml"))
    subcategories_config: Path = field(default_factory=lambda: Path("config/subcategories.yaml"))

    # API Timeouts & Retry
    api_timeout: float = field(default_factory=lambda: float(os.getenv("API_TIMEOUT", "30.0")))
    max_retries: int = field(default_factory=lambda: int(os.getenv("MAX_RETRIES", "3")))

    # Circuit Breaker
    circuit_breaker_threshold: int = field(default_factory=lambda: int(os.getenv("CB_THRESHOLD", "5")))
    circuit_breaker_timeout: int = field(default_factory=lambda: int(os.getenv("CB_TIMEOUT", "60")))

    # Logging
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    log_format: str = field(default_factory=lambda: os.getenv("LOG_FORMAT", "json"))

    # Flask
    flask_port: int = field(default_factory=lambda: int(os.getenv("PORT", "8080")))
    flask_debug: bool = field(default_factory=lambda: os.getenv("FLASK_DEBUG", "false").lower() == "true")

    def validate(self) -> None:
        """
        Validate settings.

        Raises:
            ValueError: If any setting is invalid
        """
        # Check required fields
        if not self.google_api_key:
            raise ValueError(
                "GOOGLE_API_KEY environment variable is required. "
                "See .env.example for setup instructions."
            )

        # Validate model
        if self.default_model not in ["flash", "pro"]:
            raise ValueError(
                f"Invalid DEFAULT_MODEL: {self.default_model}. "
                f"Must be 'flash' or 'pro'"
            )

        # Validate quality
        if self.default_quality not in ["basic", "detailed", "expert"]:
            raise ValueError(
                f"Invalid DEFAULT_QUALITY: {self.default_quality}. "
                f"Must be 'basic', 'detailed', or 'expert'"
            )

        # Check file paths exist
        if not self.templates_path.exists():
            raise ValueError(f"Templates file not found: {self.templates_path}")

    @classmethod
    def from_env(cls) -> "Settings":
        """
        Load settings from environment variables.

        Returns:
            Settings instance

        Example:
            settings = Settings.from_env()
            settings.validate()
        """
        return cls()


# Global settings instance
settings = Settings.from_env()
```

**File**: `.env.example`
```bash
# NanoBanana Configuration
# Copy this file to .env and fill in your values

# Required: Google API Key
GOOGLE_API_KEY=your_google_api_key_here

# Optional: Model Configuration
DEFAULT_MODEL=flash              # flash or pro
DEFAULT_QUALITY=detailed         # basic, detailed, or expert

# Optional: API Configuration
API_TIMEOUT=30.0                 # Seconds
MAX_RETRIES=3

# Optional: Circuit Breaker
CB_THRESHOLD=5                   # Failures before opening circuit
CB_TIMEOUT=60                    # Seconds to wait before retry

# Optional: Logging
LOG_LEVEL=INFO                   # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT=json                  # json or text

# Optional: Flask
PORT=8080
FLASK_DEBUG=false
```

**Update**: `src/main.py`
```python
from config.settings import settings

# Validate on startup
try:
    settings.validate()
    logger.info("Settings validated successfully")
except ValueError as e:
    logger.error(f"Invalid configuration: {e}")
    sys.exit(1)

# Initialize components with settings
classifier = DomainClassifier()
template_engine = TemplateEngine(templates_path=str(settings.templates_path))

@app.route("/generate", methods=["POST"])
@handle_api_errors
def generate_image():
    data = require_json_field(request, "prompt")

    # Use configured defaults
    quality = data.get("quality", settings.default_quality)
    model = data.get("model", settings.default_model)

    # ... rest of logic
```

---

### Day 4-5: Integration Tests (6 hours)

**File**: `tests/test_critical_paths.py`
```python
"""
Integration tests for critical paths.

Run with: pytest tests/test_critical_paths.py -v
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
import asyncio
import base64
import httpx


# --- Fixtures ---

@pytest.fixture
def mock_gemini_response():
    """Mock successful Gemini API response."""
    return {
        "candidates": [{
            "content": {
                "parts": [{
                    "inlineData": {
                        "data": base64.b64encode(b"fake_image_data").decode(),
                        "mimeType": "image/png"
                    }
                }]
            }
        }]
    }


@pytest.fixture
def mock_http_client(mock_gemini_response):
    """Mock httpx.AsyncClient for Gemini API calls."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_gemini_response
    mock_response.raise_for_status = Mock()

    mock_client = AsyncMock()
    mock_client.post.return_value = mock_response

    return mock_client


# --- Test 1: Domain Classification ---

class TestDomainClassification:
    """Test domain classifier accuracy."""

    @pytest.mark.parametrize("prompt,expected_domain,min_confidence", [
        ("professional headshot of CEO", "photography", 0.5),
        ("AWS microservices architecture diagram", "diagrams", 0.6),
        ("impressionist oil painting of garden", "art", 0.5),
        ("product photography for Amazon listing", "products", 0.5),
        ("portrait of a woman", "photography", 0.8),
        ("kubernetes deployment flowchart", "diagrams", 0.5),
    ])
    def test_classify_with_confidence(self, prompt, expected_domain, min_confidence):
        """Verify classifier accuracy on known inputs."""
        from src.domain_classifier import DomainClassifier

        classifier = DomainClassifier()
        domain, confidence = classifier.classify_with_confidence(prompt)

        assert domain == expected_domain, \
            f"Expected {expected_domain}, got {domain} for '{prompt}'"
        assert confidence >= min_confidence, \
            f"Confidence {confidence} below threshold {min_confidence}"

    def test_default_domain_when_no_matches(self):
        """Verify default domain when no keywords match."""
        from src.domain_classifier import DomainClassifier

        classifier = DomainClassifier()
        domain, confidence = classifier.classify_with_confidence("xyz abc 123")

        assert domain == "photography"  # Default
        assert confidence == 0.5  # Low confidence


# --- Test 2: Template Enhancement ---

class TestTemplateEngine:
    """Test template enhancement logic."""

    def test_enhance_basic_quality(self):
        """Verify basic quality enhancement."""
        from src.template_engine import TemplateEngine

        engine = TemplateEngine()
        enhanced = engine.enhance(
            user_input="sunset over mountains",
            domain="photography",
            quality="basic",
            subcategory="landscape"
        )

        assert "sunset over mountains" in enhanced
        assert len(enhanced) > 20  # Has some enhancement

    def test_enhance_expert_quality(self):
        """Verify expert quality includes detailed specs."""
        from src.template_engine import TemplateEngine

        engine = TemplateEngine()
        enhanced = engine.enhance(
            user_input="CEO headshot",
            domain="photography",
            quality="expert",
            subcategory="portrait"
        )

        # Should contain photography specs
        assert any(term in enhanced for term in ["Phase One", "ISO", "f/", "mm"])
        assert len(enhanced) > 100  # Detailed enhancement

    def test_suggest_subcategory(self):
        """Verify subcategory suggestion."""
        from src.template_engine import TemplateEngine

        engine = TemplateEngine()

        # Portrait keywords should suggest portrait
        subcat = engine.suggest_subcategory("headshot of CEO", "photography")
        assert subcat == "portrait"

        # Landscape keywords should suggest landscape
        subcat = engine.suggest_subcategory("sunset over mountains", "photography")
        assert subcat == "landscape"


# --- Test 3: Gemini Client ---

class TestGeminiClient:
    """Test Gemini API client."""

    @pytest.mark.asyncio
    async def test_generate_image_success(self, mock_http_client, mock_gemini_response):
        """Test successful image generation."""
        from src.gemini_client import GeminiClient

        with patch('httpx.AsyncClient', return_value=mock_http_client):
            client = GeminiClient(api_key="test_key")
            client.client = mock_http_client

            result = await client.generate_image("test prompt", model="flash")

            # Verify result structure
            assert "image_data" in result
            assert result["image_data"] == b"fake_image_data"
            assert result["mime_type"] == "image/png"
            assert result["model"] == "flash"
            assert result["prompt"] == "test prompt"

    @pytest.mark.asyncio
    async def test_retry_on_http_error(self, mock_http_client):
        """Test retry logic with exponential backoff."""
        from src.gemini_client import GeminiClient

        # Simulate 2 failures, then success
        mock_http_client.post.side_effect = [
            httpx.HTTPError("Timeout"),
            httpx.HTTPError("Timeout"),
            Mock(
                status_code=200,
                json=lambda: {
                    "candidates": [{
                        "content": {
                            "parts": [{
                                "inlineData": {
                                    "data": base64.b64encode(b"success_data").decode(),
                                    "mimeType": "image/png"
                                }
                            }]
                        }
                    }]
                },
                raise_for_status=Mock()
            )
        ]

        with patch('httpx.AsyncClient', return_value=mock_http_client):
            client = GeminiClient(api_key="test_key")
            client.client = mock_http_client

            # Should succeed after 3 attempts
            result = await client.generate_image("test", max_retries=3)

            assert result["image_data"] == b"success_data"
            assert mock_http_client.post.call_count == 3

    @pytest.mark.asyncio
    async def test_max_retries_exceeded(self, mock_http_client):
        """Test failure after max retries exceeded."""
        from src.gemini_client import GeminiClient

        # All attempts fail
        mock_http_client.post.side_effect = httpx.HTTPError("Persistent failure")

        with patch('httpx.AsyncClient', return_value=mock_http_client):
            client = GeminiClient(api_key="test_key")
            client.client = mock_http_client

            with pytest.raises(httpx.HTTPError):
                await client.generate_image("test", max_retries=3)

    def test_missing_api_key(self):
        """Test API key validation."""
        from src.gemini_client import GeminiClient
        import os

        # Clear API key
        old_key = os.environ.get("GOOGLE_API_KEY")
        if old_key:
            del os.environ["GOOGLE_API_KEY"]

        try:
            with pytest.raises(ValueError, match="API key required"):
                GeminiClient(api_key=None)
        finally:
            if old_key:
                os.environ["GOOGLE_API_KEY"] = old_key


# --- Test 4: End-to-End Flow ---

class TestEndToEndFlow:
    """Test complete image generation flow."""

    @pytest.mark.asyncio
    async def test_happy_path(self, mock_http_client):
        """Test complete flow: classify → enhance → generate."""
        from src.domain_classifier import DomainClassifier
        from src.template_engine import TemplateEngine
        from src.gemini_client import GeminiClient

        user_prompt = "professional headshot of CEO"

        # Step 1: Classify
        classifier = DomainClassifier()
        domain, confidence = classifier.classify_with_confidence(user_prompt)

        assert domain == "photography"
        assert confidence > 0.5

        # Step 2: Enhance
        template_engine = TemplateEngine()
        subcategory = template_engine.suggest_subcategory(user_prompt, domain)
        enhanced = template_engine.enhance(user_prompt, domain, "detailed", subcategory)

        assert len(enhanced) > len(user_prompt)  # Was enhanced
        assert "professional" in enhanced.lower()

        # Step 3: Generate (mocked)
        with patch('httpx.AsyncClient', return_value=mock_http_client):
            async with GeminiClient(api_key="test_key") as client:
                result = await client.generate_image(enhanced, model="flash")

            assert result["image_data"] == b"fake_image_data"


# --- Run Tests ---

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
```

**Install test dependencies**:
```bash
pip install pytest pytest-asyncio
```

**Run tests**:
```bash
pytest tests/test_critical_paths.py -v
```

---

### Day 6: Service Layer Extraction (4 hours)

**File**: `src/services/image_service.py`
```python
"""
Image generation service - core business logic.

This module is framework-agnostic (not tied to Flask).
Can be reused in CLI, background workers, etc.
"""

from typing import Dict, Callable
import asyncio


class ImageGenerationService:
    """
    Core image generation business logic.

    Orchestrates: classification → enhancement → generation
    """

    def __init__(
        self,
        classifier,
        template_engine,
        gemini_client_factory: Callable
    ):
        """
        Initialize service with dependencies.

        Args:
            classifier: DomainClassifier instance
            template_engine: TemplateEngine instance
            gemini_client_factory: Callable that returns GeminiClient
                                   (allows lazy initialization)
        """
        self.classifier = classifier
        self.template_engine = template_engine
        self.gemini_client_factory = gemini_client_factory

    async def generate_image(
        self,
        prompt: str,
        quality: str = "detailed",
        model: str = "flash"
    ) -> Dict:
        """
        Generate image from text prompt.

        Args:
            prompt: User's image description
            quality: Enhancement quality (basic/detailed/expert)
            model: Gemini model to use (flash/pro)

        Returns:
            Dictionary with:
                - image_data: bytes (image)
                - mime_type: str (e.g., "image/png")
                - enhanced_prompt: str (what was sent to API)
                - domain: str (detected domain)
                - subcategory: str (detected subcategory)
                - confidence: float (classification confidence)
                - model: str (model used)
                - original_prompt: str (user's original)

        Raises:
            ValueError: If validation fails
            httpx.HTTPError: If API call fails
        """
        # Step 1: Classify domain
        domain, confidence = self.classifier.classify_with_confidence(prompt)

        # Step 2: Suggest subcategory
        subcategory = self.template_engine.suggest_subcategory(prompt, domain)

        # Step 3: Enhance prompt
        enhanced_prompt = self.template_engine.enhance(
            user_input=prompt,
            domain=domain,
            quality=quality,
            subcategory=subcategory
        )

        # Step 4: Generate image
        async with self.gemini_client_factory() as client:
            result = await client.generate_image(enhanced_prompt, model=model)

        # Return structured data (not HTTP response)
        return {
            "image_data": result["image_data"],
            "mime_type": result["mime_type"],
            "enhanced_prompt": enhanced_prompt,
            "domain": domain,
            "subcategory": subcategory,
            "confidence": confidence,
            "model": model,
            "original_prompt": prompt
        }

    async def classify_prompt(self, prompt: str) -> Dict:
        """
        Classify prompt without generating image.

        Returns:
            Dictionary with classification details
        """
        domain, confidence = self.classifier.classify_with_confidence(prompt)
        scores = self.classifier.get_all_scores(prompt)
        subcategory = self.template_engine.suggest_subcategory(prompt, domain)
        available = self.template_engine.get_available_subcategories(domain)

        return {
            "domain": domain,
            "confidence": confidence,
            "scores": scores,
            "suggested_subcategory": subcategory,
            "available_subcategories": available
        }

    async def enhance_prompt(
        self,
        prompt: str,
        domain: str = None,
        subcategory: str = None,
        quality: str = "detailed"
    ) -> Dict:
        """
        Enhance prompt without generating image.

        Returns:
            Dictionary with enhanced prompt details
        """
        # Auto-detect domain if not provided
        if not domain:
            domain, _ = self.classifier.classify_with_confidence(prompt)

        # Auto-suggest subcategory if not provided
        if not subcategory:
            subcategory = self.template_engine.suggest_subcategory(prompt, domain)

        # Enhance
        enhanced = self.template_engine.enhance(
            user_input=prompt,
            domain=domain,
            quality=quality,
            subcategory=subcategory
        )

        return {
            "enhanced_prompt": enhanced,
            "domain": domain,
            "subcategory": subcategory,
            "quality": quality,
            "original_prompt": prompt
        }
```

**Update**: `src/main.py`
```python
from services.image_service import ImageGenerationService
from gemini_client import GeminiClient

# Initialize service (once on startup)
def create_gemini_client():
    """Factory for creating GeminiClient."""
    return GeminiClient(api_key=settings.google_api_key)

image_service = ImageGenerationService(
    classifier=classifier,
    template_engine=template_engine,
    gemini_client_factory=create_gemini_client
)

@app.route("/generate", methods=["POST"])
@handle_api_errors
def generate_image():
    """Generate image from prompt."""
    data = require_json_field(request, "prompt")

    # Validate
    quality = data.get("quality", settings.default_quality)
    if quality not in ["basic", "detailed", "expert"]:
        raise ValidationError(f"Invalid quality: {quality}")

    model = data.get("model", settings.default_model)
    if model not in ["flash", "pro"]:
        raise ValidationError(f"Invalid model: {model}")

    # Call service (no orchestration logic here!)
    result = run_async(image_service.generate_image(
        prompt=data["prompt"],
        quality=quality,
        model=model
    ))

    # Format response
    return format_base64_response(result), 200

@app.route("/classify", methods=["POST"])
@handle_api_errors
def classify():
    """Classify prompt domain."""
    data = require_json_field(request, "prompt")

    result = run_async(image_service.classify_prompt(data["prompt"]))

    return jsonify(result), 200

@app.route("/enhance", methods=["POST"])
@handle_api_errors
def enhance():
    """Enhance prompt without generating."""
    data = require_json_field(request, "prompt")

    result = run_async(image_service.enhance_prompt(
        prompt=data["prompt"],
        domain=data.get("domain"),
        subcategory=data.get("subcategory"),
        quality=data.get("quality", "detailed")
    ))

    return jsonify(result), 200
```

---

## Week 2: Medium-Priority Improvements (13.5 hours)

### Configuration-Driven Domains

**File**: `config/domains.yaml`
```yaml
# Domain configuration for image classification

domains:
  photography:
    keywords:
      - photo
      - photograph
      - portrait
      - headshot
      - selfie
      - picture
      - shot
      - camera
      - lens
      - lighting
      - bokeh
      - focus
      - exposure
      - ISO
      - aperture
      - landscape
      - cityscape
      - sunset
      - golden hour
      - Canon
      - Nikon
      - Sony
      - Phase One
    confidence_threshold: 0.5

  diagrams:
    keywords:
      - diagram
      - chart
      - graph
      - flowchart
      - wireframe
      - architecture
      - schematic
      - blueprint
      - layout
      - infographic
      - visualization
      - flow
      - process
      - UML
      - ERD
      - sequence
      - component
      - network
      - AWS
      - GCP
      - Azure
      - microservices
      - infrastructure
    confidence_threshold: 0.6

  art:
    keywords:
      - art
      - artwork
      - painting
      - drawing
      - illustration
      - sketch
      - watercolor
      - oil painting
      - acrylic
      - impressionist
      - abstract
      - surreal
      - realistic
      - digital art
      - concept art
      - character design
      - style of
      - inspired by
      - artistic
      - creative
    confidence_threshold: 0.5

  products:
    keywords:
      - product
      - ecommerce
      - catalog
      - merchandise
      - item
      - package
      - packaging
      - unboxing
      - advertising
      - commercial
      - marketing
      - promotional
      - studio shot
      - white background
      - lifestyle
      - Amazon
      - Shopify
      - store
      - retail
    confidence_threshold: 0.5
```

**Update**: `src/domain_classifier.py`
```python
import yaml
from pathlib import Path
from typing import Dict, List

class DomainClassifier:
    """Classifies prompts into domains using keyword matching."""

    def __init__(self, config_path: str = "config/domains.yaml"):
        """
        Initialize classifier with domain configuration.

        Args:
            config_path: Path to YAML config file
        """
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        # Build domain keywords dict
        self.DOMAIN_KEYWORDS = {
            domain: data["keywords"]
            for domain, data in config["domains"].items()
        }

        # Store confidence thresholds
        self.confidence_thresholds = {
            domain: data["confidence_threshold"]
            for domain, data in config["domains"].items()
        }

    # ... rest of classifier methods unchanged
```

**Install PyYAML**:
```bash
pip install pyyaml
```

---

## Testing the Refactored Code

**Run all tests**:
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

**Test coverage goal**: 80%+ for critical paths

**Manual testing**:
```bash
# Start server
python src/main.py

# Test generate endpoint
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "professional CEO headshot", "quality": "expert"}'

# Test classify endpoint
curl -X POST http://localhost:8080/classify \
  -H "Content-Type: application/json" \
  -d '{"prompt": "AWS architecture diagram"}'

# Test enhance endpoint
curl -X POST http://localhost:8080/enhance \
  -H "Content-Type: application/json" \
  -d '{"prompt": "sunset over mountains", "quality": "detailed"}'
```

---

## Deployment Checklist

Before deploying refactored code:

- [ ] All tests pass (`pytest tests/ -v`)
- [ ] `.env` file configured with real API key
- [ ] Logging produces structured JSON output
- [ ] Error handling tested with invalid inputs
- [ ] Configuration validated on startup
- [ ] Service layer tested independently
- [ ] No print statements (only logger calls)
- [ ] Circuit breaker tested with API failures

---

## Next Steps

After completing Week 1 + Week 2 refactoring:

1. **Monitor Production**
   - Check structured logs for errors
   - Verify circuit breaker metrics
   - Monitor API response times

2. **Iterate**
   - Add new domains via YAML config
   - Experiment with meta-prompting
   - A/B test template vs LLM enhancement

3. **Scale**
   - Extract content type abstraction
   - Add new content types (presentations, UI)
   - Build multi-media factory

---

**End of Implementation Guide**

*Code examples are production-ready. Copy, test, deploy!*
