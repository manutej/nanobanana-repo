#!/usr/bin/env python3
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
import main as api_main  # noqa: E402


class FakeGeminiClient:
    ASPECT_RATIOS = {"1:1", "16:9", "9:16", "4:3", "3:4"}
    IMAGE_SIZES = {"1K", "2K", "4K"}

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return False

    async def generate_image(
        self,
        prompt,
        model="flash",
        aspect_ratio=None,
        image_size=None,
        max_retries=3
    ):
        if aspect_ratio and aspect_ratio not in self.ASPECT_RATIOS:
            raise ValueError("Invalid aspect_ratio")
        if image_size and image_size not in self.IMAGE_SIZES:
            raise ValueError("Invalid image_size")

        return {
            "image_data": b"fake-image-bytes",
            "mime_type": "image/png",
            "model": model,
            "prompt": prompt
        }


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(api_main, "GeminiClient", FakeGeminiClient)
    api_main.app.config["TESTING"] = True
    with api_main.app.test_client() as test_client:
        yield test_client


def test_generate_supports_brand_aspect_and_size(client):
    response = client.post(
        "/generate",
        json={
            "prompt": "professional product photo",
            "quality": "detailed",
            "model": "flash",
            "aspect_ratio": "16:9",
            "image_size": "2K",
            "brand_profile": "modern_tech"
        }
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["image"].startswith("data:image/png;base64,")
    assert body["metadata"]["aspect_ratio"] == "16:9"
    assert body["metadata"]["image_size"] == "2K"
    assert body["metadata"]["brand_profile"] == "modern_tech"
    assert "brand tone:" in body["enhanced_prompt"]
    expected_tone = api_main.brand_profile_manager.get_profile("modern_tech")["tone"]
    assert f"brand tone: {expected_tone}" in body["enhanced_prompt"]


def test_batch_endpoint_returns_per_item_status(client):
    response = client.post(
        "/generate/batch",
        json={
            "max_concurrent": 2,
            "requests": [
                {
                    "prompt": "cloud architecture diagram",
                    "model": "pro",
                    "aspect_ratio": "1:1"
                },
                {
                    "prompt": "wireframe mockup",
                    "quality": "invalid-quality"
                }
            ]
        }
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["total"] == 2
    assert body["succeeded"] == 1
    assert body["failed"] == 1
    assert body["results"][0]["status"] in {"success", "error"}
    assert body["results"][1]["status"] in {"success", "error"}


def test_brand_profiles_endpoint(client):
    response = client.get("/brand-profiles")
    assert response.status_code == 200
    body = response.get_json()
    assert "available_profiles" in body
    assert "modern_tech" in body["available_profiles"]


def test_enhance_applies_brand_profile(client):
    response = client.post(
        "/enhance",
        json={
            "prompt": "enterprise SaaS landing page hero image",
            "quality": "detailed",
            "brand_profile": "luxury_editorial"
        }
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["brand_profile"] == "luxury_editorial"
    assert "brand tone:" in body["enhanced_prompt"]
    expected_tone = api_main.brand_profile_manager.get_profile("luxury_editorial")["tone"]
    assert f"brand tone: {expected_tone}" in body["enhanced_prompt"]
