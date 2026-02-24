#!/usr/bin/env python3
"""
Test the REAL image generation models that were discovered in the API listing.

These models actually exist:
- models/gemini-2.5-flash-image (Nano Banana)
- models/gemini-3-pro-image-preview (Nano Banana Pro)
- models/nano-banana-pro-preview (Nano Banana Pro)
- models/imagen-4.0-generate-001 (Imagen 4)
- models/imagen-4.0-ultra-generate-001 (Imagen 4 Ultra)
- models/imagen-4.0-fast-generate-001 (Imagen 4 Fast)
"""

import os
import json
import httpx
from pathlib import Path


def test_gemini_flash_image():
    """Test Gemini 2.5 Flash Image (Nano Banana)."""
    api_key = os.getenv('GOOGLE_API_KEY')

    # Try different request formats
    formats = [
        {
            "name": "generateContent format",
            "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent",
            "body": {
                "contents": [{
                    "parts": [{
                        "text": "Generate an image of a cute yellow banana wearing sunglasses on a beach"
                    }]
                }]
            }
        },
        {
            "name": "predict format",
            "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:predict",
            "body": {
                "instances": [{
                    "prompt": "A cute yellow banana wearing sunglasses on a beach"
                }]
            }
        },
        {
            "name": "direct format",
            "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image",
            "body": {
                "prompt": "A cute yellow banana wearing sunglasses on a beach"
            }
        }
    ]

    print("=" * 80)
    print("Testing: models/gemini-2.5-flash-image (Nano Banana)")
    print("=" * 80)

    for fmt in formats:
        print(f"\nTrying {fmt['name']}...")
        print(f"Endpoint: {fmt['endpoint']}")

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    f"{fmt['endpoint']}?key={api_key}",
                    json=fmt['body'],
                    headers={"Content-Type": "application/json"}
                )

                print(f"Status: {response.status_code}")

                if response.status_code in [200, 201]:
                    print("✅ SUCCESS!")
                    print("Response:")
                    print(json.dumps(response.json(), indent=2)[:1000])
                    return True
                else:
                    print(f"❌ Failed: {response.text[:500]}")

        except Exception as e:
            print(f"❌ Error: {e}")

    return False


def test_imagen_4():
    """Test Imagen 4 models."""
    api_key = os.getenv('GOOGLE_API_KEY')

    models = [
        "imagen-4.0-generate-001",
        "imagen-4.0-fast-generate-001",
        "imagen-4.0-ultra-generate-001"
    ]

    print("\n" + "=" * 80)
    print("Testing: Imagen 4 Models")
    print("=" * 80)

    for model in models:
        print(f"\n{model}...")

        # Try predict method (as shown in model listing)
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:predict"

        # Try multiple request body formats
        bodies = [
            {
                "instances": [{
                    "prompt": "A cute yellow banana wearing sunglasses on a beach"
                }],
                "parameters": {
                    "sampleCount": 1
                }
            },
            {
                "prompt": "A cute yellow banana wearing sunglasses on a beach",
                "sampleCount": 1
            },
            {
                "contents": [{
                    "parts": [{
                        "text": "A cute yellow banana wearing sunglasses on a beach"
                    }]
                }]
            }
        ]

        for i, body in enumerate(bodies, 1):
            try:
                with httpx.Client(timeout=30.0) as client:
                    response = client.post(
                        f"{endpoint}?key={api_key}",
                        json=body,
                        headers={"Content-Type": "application/json"}
                    )

                    print(f"  Format {i}: Status {response.status_code}")

                    if response.status_code in [200, 201]:
                        print("  ✅ SUCCESS!")
                        print("  Response:")
                        print(json.dumps(response.json(), indent=2)[:1000])
                        return True
                    elif response.status_code == 400:
                        error_data = response.json()
                        if 'error' in error_data:
                            print(f"  ❌ {error_data['error'].get('message', '')[:200]}")
                    else:
                        print(f"  ❌ {response.text[:200]}")

            except Exception as e:
                print(f"  ❌ Error: {e}")

    return False


def test_nano_banana_pro():
    """Test Nano Banana Pro models."""
    api_key = os.getenv('GOOGLE_API_KEY')

    models = [
        "gemini-3-pro-image-preview",
        "nano-banana-pro-preview"
    ]

    print("\n" + "=" * 80)
    print("Testing: Nano Banana Pro Models")
    print("=" * 80)

    for model in models:
        print(f"\n{model}...")

        # These support generateContent according to listing
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

        body = {
            "contents": [{
                "parts": [{
                    "text": "Generate an image of a cute yellow banana wearing sunglasses on a beach"
                }]
            }]
        }

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    f"{endpoint}?key={api_key}",
                    json=body,
                    headers={"Content-Type": "application/json"}
                )

                print(f"Status: {response.status_code}")

                if response.status_code in [200, 201]:
                    print("✅ SUCCESS!")
                    print("Response:")
                    result = response.json()
                    print(json.dumps(result, indent=2)[:2000])
                    return True
                else:
                    print(f"❌ Failed: {response.text[:500]}")

        except Exception as e:
            print(f"❌ Error: {e}")

    return False


def main():
    """Run all tests."""
    print("TESTING REAL IMAGE GENERATION MODELS")
    print("=" * 80)
    print()

    success = False

    # Test 1: Gemini Flash Image (Nano Banana)
    if test_gemini_flash_image():
        success = True

    # Test 2: Imagen 4
    if test_imagen_4():
        success = True

    # Test 3: Nano Banana Pro
    if test_nano_banana_pro():
        success = True

    print("\n" + "=" * 80)
    if success:
        print("✅ AT LEAST ONE MODEL WORKS!")
    else:
        print("❌ NO MODELS WORKED")
        print("\nPossible reasons:")
        print("1. These models exist but require special access/billing")
        print("2. The request format is different than expected")
        print("3. The API key doesn't have permission")
        print("4. Models are listed but not yet available")
    print("=" * 80)


if __name__ == "__main__":
    main()
