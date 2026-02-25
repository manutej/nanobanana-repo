"""
Tests for the Flask API endpoints in main.py.

Validates the parse_prompt_request helper and endpoint behavior.
"""

import json
import sys
from pathlib import Path
from unittest.mock import patch, AsyncMock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import app, parse_prompt_request


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestParsePromptRequest:
    """Tests for the parse_prompt_request helper."""

    def test_missing_json_body(self, client):
        with app.test_request_context(content_type="application/json", data="null"):
            data, error = parse_prompt_request()
            assert data is None
            assert error is not None

    def test_missing_prompt_key(self, client):
        with app.test_request_context(
            content_type="application/json", data=json.dumps({"text": "hello"})
        ):
            data, error = parse_prompt_request()
            assert data is None
            assert error is not None

    def test_valid_request(self, client):
        with app.test_request_context(
            content_type="application/json",
            data=json.dumps({"prompt": "sunset"}),
        ):
            data, error = parse_prompt_request()
            assert error is None
            assert data["prompt"] == "sunset"


class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "healthy"


class TestClassifyEndpoint:
    def test_classify_returns_domain(self, client):
        response = client.post(
            "/classify",
            data=json.dumps({"prompt": "headshot of a CEO"}),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["domain"] == "photography"
        assert "confidence" in data
        assert "scores" in data

    def test_classify_missing_prompt(self, client):
        response = client.post(
            "/classify",
            data=json.dumps({"text": "hello"}),
            content_type="application/json",
        )
        assert response.status_code == 400


class TestEnhanceEndpoint:
    def test_enhance_returns_enhanced_prompt(self, client):
        response = client.post(
            "/enhance",
            data=json.dumps({"prompt": "headshot of a CEO", "quality": "basic"}),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "enhanced_prompt" in data
        assert "headshot of a CEO" in data["enhanced_prompt"]

    def test_enhance_missing_prompt(self, client):
        response = client.post(
            "/enhance",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert response.status_code == 400


class TestGenerateEndpoint:
    def test_generate_missing_prompt(self, client):
        response = client.post(
            "/generate",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_generate_invalid_quality(self, client):
        response = client.post(
            "/generate",
            data=json.dumps({"prompt": "test", "quality": "ultra"}),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_generate_invalid_model(self, client):
        response = client.post(
            "/generate",
            data=json.dumps({"prompt": "test", "model": "invalid"}),
            content_type="application/json",
        )
        assert response.status_code == 400
