"""
Simple Async Batch Image Generation - The Elegant Solution

Based on comonadic extraction: separate core operation (generate one image)
from batch orchestration (streaming, concurrency control).

Uses Python's asyncio primitives - no magic, no over-engineering.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import asyncio
from typing import List, Dict, AsyncGenerator
from pathlib import Path
from gemini_client import GeminiClient


async def generate_batch_streaming(
    prompts: List[str],
    max_concurrent: int = 5
) -> AsyncGenerator[Dict, None]:
    """
    Generate images concurrently, yield results as they complete.

    Core insight: Keep the local operation (generate one image) separate
    from the context (semaphore, streaming).

    Args:
        prompts: List of text prompts
        max_concurrent: Max concurrent API calls

    Yields:
        Results in completion order (not input order)
    """
    semaphore = asyncio.Semaphore(max_concurrent)

    async def generate_one(prompt: str, index: int) -> Dict:
        """The core operation - generate single image"""
        async with semaphore:
            async with GeminiClient() as client:
                result = await client.generate_image(prompt, model="flash")
                return {
                    "index": index,
                    "prompt": prompt,
                    "image_data": result["image_data"],
                    "size_mb": len(result["image_data"]) / (1024 * 1024),
                    "status": "success"
                }

    # Create all tasks
    tasks = [generate_one(p, i) for i, p in enumerate(prompts)]

    # Yield results as they complete (streaming)
    for coro in asyncio.as_completed(tasks):
        try:
            yield await coro
        except Exception as e:
            # Yield error without stopping the batch
            yield {
                "status": "error",
                "error": str(e)
            }


async def main():
    """Test the simple batch generator"""

    # 10 diverse prompts
    prompts = [
        "Professional headshot of a female CEO in her 40s",
        "Sunset over mountains with a lake in foreground",
        "Wireless headphones for Amazon listing",
        "Garden with flowers in impressionist style",
        "Cloud-native microservices architecture diagram",
        "User authentication flow with OAuth2",
        "Mobile app wireframe for image generation",
        "Futuristic sports car in studio",
        "Coffee mug being held while reading by window",
        "Tech startup team brainstorming session"
    ]

    # Output directory
    output_dir = Path("examples/simple_batch_images")
    output_dir.mkdir(exist_ok=True)

    print("🍌 Simple Batch Image Generation")
    print("=" * 70)
    print(f"Prompts: {len(prompts)}")
    print(f"Max Concurrent: 5")
    print(f"Output: {output_dir}")
    print()

    completed = 0
    succeeded = 0
    failed = 0

    # Stream results as they complete
    async for result in generate_batch_streaming(prompts, max_concurrent=5):
        completed += 1

        if result["status"] == "success":
            succeeded += 1

            # Save image
            filename = f"{result['index']:02d}_{result['prompt'][:30].replace(' ', '_')}.png"
            filepath = output_dir / filename

            with open(filepath, "wb") as f:
                f.write(result["image_data"])

            print(
                f"✓ [{completed}/{len(prompts)}] "
                f"{result['size_mb']:.2f} MB - {result['prompt'][:50]}..."
            )
            print(f"  → {filepath}")

        else:
            failed += 1
            print(f"✗ [{completed}/{len(prompts)}] Error: {result.get('error', 'Unknown')}")

    # Summary
    print()
    print("=" * 70)
    print("📊 Batch Complete")
    print(f"  Total: {len(prompts)}")
    print(f"  Succeeded: {succeeded} ✓")
    print(f"  Failed: {failed} ✗")
    print(f"  Success Rate: {succeeded / len(prompts) * 100:.1f}%")
    print()


if __name__ == "__main__":
    # Load API key from environment
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ ERROR: GOOGLE_API_KEY not set")
        print("Run: export GOOGLE_API_KEY='your_key_here'")
        sys.exit(1)

    asyncio.run(main())
