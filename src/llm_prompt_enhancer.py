#!/usr/bin/env python3
"""
LLM-Based Prompt Enhancement

Uses Gemini's text model to intelligently analyze and enhance image prompts
before calling the image generation API. This replaces brittle keyword matching
with dynamic, context-aware prompt improvement.
"""

import asyncio
import httpx
import json
import os
from typing import Dict, Tuple, Optional


class LLMPromptEnhancer:
    """
    Intelligent prompt enhancement using Gemini text model.

    Uses a two-step process:
    1. Analyze prompt with Gemini text model (fast, cheap)
    2. Get structured enhancement instructions
    3. Apply enhancements and return optimized prompt
    """

    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
    TEXT_MODEL = "gemini-pro"  # Fast, cheap text model for analysis

    ENHANCEMENT_PROMPT = """You are an expert prompt engineer for image generation APIs.
Your task is to analyze a user's image request and provide an enhanced, professionally-specified prompt.

User's Request: "{user_prompt}"

Analyze this request and provide:

1. DOMAIN: What type of image is this?
   - photography (real photos with camera specs)
   - diagrams (technical diagrams, charts, architecture)
   - art (paintings, digital art, illustrations)
   - products (product photography, e-commerce)

2. STYLE: What specific style or subcategory?
   - For photography: portrait, landscape, product, macro, architectural
   - For diagrams: architecture, flowchart, wireframe, sequence, technical
   - For art: painting, digital_art, 3d_render, abstract, impressionist, cubist
   - For products: ecommerce, lifestyle, editorial, advertising

3. ENHANCEMENT: Rewrite the prompt with professional specifications.

   Guidelines:
   - For PHOTOGRAPHY: Add camera specs (sensor, lens, ISO, aperture), lighting setup, composition rules
   - For DIAGRAMS: Add style guides (AWS/GCP docs, BPMN, UML), color coding, annotations, layout
   - For ART: Add artistic style references, techniques, composition, color palette, mood
   - For PRODUCTS: Add lighting, background, angle, product styling, brand aesthetics

4. CONFIDENCE: How confident are you in the domain/style classification? (0.0-1.0)

Respond ONLY with valid JSON in this exact format:
{{
  "domain": "photography|diagrams|art|products",
  "style": "specific style from list above",
  "confidence": 0.95,
  "enhanced_prompt": "fully enhanced professional prompt here with 100-200 words of specifications",
  "reasoning": "brief explanation of why you chose this domain/style"
}}

Be creative and specific. Add details that would make a professional-quality image."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize with Google API key."""
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("API key required. Set GOOGLE_API_KEY environment variable")

        self.client = None

    async def __aenter__(self):
        """Async context manager entry."""
        self.client = httpx.AsyncClient(timeout=30.0)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.client:
            await self.client.aclose()

    async def enhance_prompt(
        self,
        user_prompt: str,
        max_retries: int = 3
    ) -> Dict[str, any]:
        """
        Enhance user prompt using LLM analysis.

        Args:
            user_prompt: User's original image request
            max_retries: Number of retries on failure

        Returns:
            Dictionary with:
                - domain: str (photography/diagrams/art/products)
                - style: str (specific subcategory)
                - confidence: float (0.0-1.0)
                - enhanced_prompt: str (professional prompt)
                - reasoning: str (why this classification)
                - original_prompt: str (user's original)

        Raises:
            ValueError: If API key missing or response invalid
            httpx.HTTPError: If API call fails after retries
        """
        if not self.client:
            raise ValueError("Must use async context manager (async with)")

        # Construct analysis prompt
        analysis_prompt = self.ENHANCEMENT_PROMPT.format(user_prompt=user_prompt)

        endpoint = f"{self.BASE_URL}/{self.TEXT_MODEL}:generateContent"

        payload = {
            "contents": [{
                "parts": [{"text": analysis_prompt}]
            }],
            "generationConfig": {
                "temperature": 0.3,  # Lower = more consistent
                "topP": 0.9,
                "topK": 40,
                "maxOutputTokens": 2048
            }
        }

        # Retry logic with exponential backoff
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

                # Extract text response (handle multi-part)
                parts = data["candidates"][0]["content"]["parts"]
                text_response = None

                for part in parts:
                    if "text" in part:
                        text_response = part["text"]
                        break

                if not text_response:
                    raise ValueError("No text response from LLM")

                # Parse JSON response
                # Handle markdown code blocks if present
                json_text = text_response.strip()
                if json_text.startswith("```json"):
                    json_text = json_text.split("```json")[1].split("```")[0].strip()
                elif json_text.startswith("```"):
                    json_text = json_text.split("```")[1].split("```")[0].strip()

                enhancement = json.loads(json_text)

                # Validate required fields
                required = ["domain", "style", "confidence", "enhanced_prompt"]
                for field in required:
                    if field not in enhancement:
                        raise ValueError(f"Missing required field: {field}")

                # Add original prompt for reference
                enhancement["original_prompt"] = user_prompt

                # Validate domain
                valid_domains = ["photography", "diagrams", "art", "products"]
                if enhancement["domain"] not in valid_domains:
                    raise ValueError(f"Invalid domain: {enhancement['domain']}")

                # Validate confidence
                if not (0.0 <= enhancement["confidence"] <= 1.0):
                    raise ValueError(f"Invalid confidence: {enhancement['confidence']}")

                return enhancement

            except (httpx.HTTPError, json.JSONDecodeError, ValueError) as e:
                if attempt == max_retries - 1:
                    # Last attempt failed
                    raise ValueError(f"LLM enhancement failed after {max_retries} attempts: {e}")

                # Exponential backoff
                await asyncio.sleep(2 ** attempt)

        # Should never reach here
        raise ValueError("Enhancement failed unexpectedly")

    async def batch_enhance(
        self,
        prompts: list[str]
    ) -> list[Dict[str, any]]:
        """
        Enhance multiple prompts in parallel.

        Args:
            prompts: List of user prompts

        Returns:
            List of enhancement dictionaries
        """
        tasks = [self.enhance_prompt(prompt) for prompt in prompts]
        return await asyncio.gather(*tasks, return_exceptions=True)


async def demo():
    """Demo the LLM-based enhancement."""

    test_prompts = [
        "professional headshot of a CEO",
        "Garden with flowers in impressionist style",
        "Kubernetes architecture diagram with GitOps",
        "Wireless headphones for Amazon listing",
        "Cyberpunk street scene with neon lights"
    ]

    print("🤖 LLM-Based Prompt Enhancement Demo")
    print("=" * 70)

    async with LLMPromptEnhancer() as enhancer:
        for i, prompt in enumerate(test_prompts, 1):
            print(f"\n{i}. Original: \"{prompt}\"")

            try:
                result = await enhancer.enhance_prompt(prompt)

                print(f"   Domain: {result['domain']}")
                print(f"   Style: {result['style']}")
                print(f"   Confidence: {result['confidence']:.2f}")
                print(f"   Reasoning: {result['reasoning']}")
                print(f"   Enhanced: {result['enhanced_prompt'][:100]}...")

            except Exception as e:
                print(f"   ❌ Error: {e}")

    print("\n" + "=" * 70)
    print("Demo complete!")


if __name__ == "__main__":
    asyncio.run(demo())
