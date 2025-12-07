"""
Gemini API Client - Simple HTTP wrapper for image generation

Calls Google's Gemini Image Generation API (gemini-2.5-flash-image).
This is just httpx.post() - no "functorial abstraction" jargon needed!
"""

import asyncio
import base64
import os
from typing import Optional, Dict
import httpx


class GeminiClient:
    """
    Simple client for Gemini image generation API.

    Example:
        client = GeminiClient(api_key=os.getenv("GOOGLE_API_KEY"))
        result = await client.generate_image("a cute banana on a beach")
        image_bytes = result["image_data"]
    """

    # API endpoint - verified working!
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"

    # Available models (verified working)
    MODELS = {
        "flash": "gemini-2.5-flash-image",  # Fast, cheap
        "pro": "gemini-3-pro-image-preview"  # Higher quality
    }

    def __init__(self, api_key: Optional[str] = None, timeout: float = 30.0):
        """
        Initialize Gemini client.

        Args:
            api_key: Google API key (defaults to GOOGLE_API_KEY env var)
            timeout: Request timeout in seconds (default: 30.0)
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key required. Set GOOGLE_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)

    async def generate_image(
        self,
        prompt: str,
        model: str = "flash",
        max_retries: int = 3
    ) -> Dict:
        """
        Generate image from text prompt.

        Args:
            prompt: Text description of image to generate
            model: "flash" (fast) or "pro" (high quality)
            max_retries: Number of retries on failure

        Returns:
            Dictionary with:
                - image_data: bytes (PNG image data)
                - mime_type: str (e.g., "image/png")
                - model: str (model used)
                - prompt: str (original prompt)

        Raises:
            ValueError: If model is invalid
            httpx.HTTPError: If API call fails after retries

        Example:
            result = await client.generate_image(
                "professional headshot of a CEO",
                model="flash"
            )
            with open("output.png", "wb") as f:
                f.write(result["image_data"])
        """
        # Validate model
        if model not in self.MODELS:
            raise ValueError(
                f"Invalid model: {model}. Must be one of {list(self.MODELS.keys())}"
            )

        model_id = self.MODELS[model]
        endpoint = f"{self.BASE_URL}/{model_id}:generateContent"

        # Request payload
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        # Retry loop with exponential backoff
        for attempt in range(max_retries):
            try:
                response = await self.client.post(
                    endpoint,
                    params={"key": self.api_key},
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )

                response.raise_for_status()
                data = response.json()

                # Extract image from response
                # Note: API may return multiple parts (text + image)
                # We need to find the part with inlineData
                parts = data["candidates"][0]["content"]["parts"]

                image_b64 = None
                mime_type = None

                for part in parts:
                    if "inlineData" in part:
                        image_b64 = part["inlineData"]["data"]
                        mime_type = part["inlineData"]["mimeType"]
                        break

                if not image_b64:
                    raise ValueError(
                        f"No image data found in response. "
                        f"API returned {len(parts)} parts but none contained inlineData"
                    )

                # Decode base64
                image_bytes = base64.b64decode(image_b64)

                return {
                    "image_data": image_bytes,
                    "mime_type": mime_type,
                    "model": model,
                    "prompt": prompt
                }

            except httpx.HTTPError as e:
                # Retry on failure
                if attempt == max_retries - 1:
                    raise  # Last attempt, give up

                # Exponential backoff
                wait_time = 2 ** attempt
                print(f"API call failed (attempt {attempt + 1}/{max_retries}): {e}")
                print(f"Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)

    async def generate_and_save(
        self,
        prompt: str,
        output_path: str,
        model: str = "flash"
    ) -> str:
        """
        Generate image and save to file (convenience method).

        Args:
            prompt: Text description
            output_path: Where to save image
            model: "flash" or "pro"

        Returns:
            Path to saved file

        Example:
            path = await client.generate_and_save(
                "sunset over mountains",
                "sunset.png",
                model="pro"
            )
            print(f"Saved to {path}")
        """
        result = await self.generate_image(prompt, model)

        with open(output_path, "wb") as f:
            f.write(result["image_data"])

        return output_path

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


# Convenience function for simple usage
async def generate_image(
    prompt: str,
    model: str = "flash",
    api_key: Optional[str] = None
) -> bytes:
    """
    Quick image generation function - use this for simple cases.

    Args:
        prompt: Text description
        model: "flash" or "pro"
        api_key: Optional API key

    Returns:
        Image data as bytes

    Example:
        image_data = await generate_image("a red ball")
        with open("ball.png", "wb") as f:
            f.write(image_data)
    """
    async with GeminiClient(api_key=api_key) as client:
        result = await client.generate_image(prompt, model)
        return result["image_data"]


if __name__ == "__main__":
    # Quick test
    async def test():
        client = GeminiClient()

        print("Testing Gemini Image Generation API\n")

        # Test flash model
        print("1. Testing Flash model...")
        result = await client.generate_image(
            "a simple red ball on white background",
            model="flash"
        )
        print(f"✓ Generated {len(result['image_data'])} bytes ({result['mime_type']})")

        # Save test image
        output_path = "test_output.png"
        await client.generate_and_save(
            "a cute yellow banana wearing sunglasses",
            output_path,
            model="flash"
        )
        print(f"✓ Saved test image to {output_path}")

        await client.close()
        print("\n✅ All tests passed!")

    # Run test
    asyncio.run(test())
