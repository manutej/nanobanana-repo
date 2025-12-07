#!/usr/bin/env python3
"""
Generate a proof-of-concept image to demonstrate the API actually works.
"""

import os
import httpx
import base64
from pathlib import Path


def generate_banana_image(prompt: str, api_key: str) -> bytes:
    """Generate an image using Gemini 2.5 Flash Image (Nano Banana)."""

    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent"

    request_body = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }

    print(f"Generating image with prompt: '{prompt}'")
    print(f"Using endpoint: {endpoint}")
    print()

    with httpx.Client(timeout=30.0) as client:
        response = client.post(
            f"{endpoint}?key={api_key}",
            json=request_body,
            headers={"Content-Type": "application/json"}
        )

        print(f"Response status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()

            # Extract image data from response
            for part in data["candidates"][0]["content"]["parts"]:
                if "inlineData" in part:
                    image_b64 = part["inlineData"]["data"]
                    image_mime = part["inlineData"]["mimeType"]
                    print(f"Image MIME type: {image_mime}")
                    print(f"Base64 length: {len(image_b64)} chars")
                    return base64.b64decode(image_b64)

            raise ValueError("No image data in response")
        else:
            raise Exception(f"API error: {response.status_code} - {response.text}")


def main():
    api_key = os.getenv('GOOGLE_API_KEY')

    if not api_key:
        print("ERROR: GOOGLE_API_KEY not set")
        return

    # Generate image
    prompt = "A cute yellow banana character wearing stylish sunglasses, relaxing on a tropical beach. The banana has a happy friendly face, and the scene is colorful and fun. Digital art style."

    print("=" * 80)
    print("GENERATING PROOF-OF-CONCEPT IMAGE")
    print("=" * 80)
    print()

    try:
        image_bytes = generate_banana_image(prompt, api_key)

        # Save to file
        output_path = Path("/Users/manu/Documents/LUXOR/PROJECTS/nanobanana-repo/PROOF_IMAGE.png")
        output_path.write_bytes(image_bytes)

        print()
        print("=" * 80)
        print("✅ SUCCESS!")
        print("=" * 80)
        print(f"Image saved to: {output_path}")
        print(f"Image size: {len(image_bytes):,} bytes")
        print()
        print("This proves the NanoBanana API exists and works!")

    except Exception as e:
        print()
        print("=" * 80)
        print("❌ FAILED")
        print("=" * 80)
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
