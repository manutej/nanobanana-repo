#!/usr/bin/env python3
"""
Debug script to inspect actual API responses for failed examples.
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from domain_classifier import DomainClassifier
from template_engine import TemplateEngine
import httpx


async def test_api_response(prompt: str, quality: str = "expert"):
    """Test a single prompt and print full API response."""

    # Initialize components
    classifier = DomainClassifier()
    template_engine = TemplateEngine()

    # Classify and enhance
    domain, confidence = classifier.classify_with_confidence(prompt)
    subcategory = template_engine.suggest_subcategory(prompt, domain)
    enhanced = template_engine.enhance(prompt, domain, quality, subcategory)

    print(f"\n{'='*70}")
    print(f"Testing: {prompt[:60]}...")
    print(f"{'='*70}")
    print(f"Domain: {domain} (confidence: {confidence:.2f})")
    print(f"Subcategory: {subcategory}")
    print(f"Enhanced: {enhanced[:200]}...")
    print()

    # Call API directly
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ No API key found!")
        return

    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent"

    payload = {
        "contents": [{
            "parts": [{"text": enhanced}]
        }]
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                endpoint,
                params={"key": api_key},
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            response.raise_for_status()
            data = response.json()

            print("✅ API Response:")
            print(json.dumps(data, indent=2))
            print()

            # Check structure
            if "candidates" in data:
                candidate = data["candidates"][0]
                print(f"Candidate keys: {list(candidate.keys())}")

                if "content" in candidate:
                    content = candidate["content"]
                    print(f"Content keys: {list(content.keys())}")

                    if "parts" in content and len(content["parts"]) > 0:
                        part = content["parts"][0]
                        print(f"Part keys: {list(part.keys())}")

                        if "inlineData" in part:
                            print("✓ Has inlineData - SUCCESS!")
                        else:
                            print("✗ Missing inlineData - FAILURE!")
                            if "text" in part:
                                print(f"Text response: {part['text'][:200]}")

        except Exception as e:
            print(f"❌ Error: {e}")
            if hasattr(e, 'response'):
                print(f"Response: {e.response.text}")


async def main():
    """Test multiple failed examples."""

    # Test cases that failed
    test_cases = [
        ("Professional headshot of a female CEO in her 40s", "expert"),
        ("Sunset over mountains with a lake in foreground", "expert"),
        ("Wireless headphones for Amazon listing", "detailed"),
        ("User authentication flow with OAuth2 and error handling", "expert"),  # This is a diagram!
    ]

    for prompt, quality in test_cases:
        await test_api_response(prompt, quality)
        print("\n" + "="*70 + "\n")

    print("Debug complete!")


if __name__ == "__main__":
    asyncio.run(main())
