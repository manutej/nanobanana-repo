#!/usr/bin/env python3
"""
Generate Abstract Symbolic Concept images using Gemini 3 Pro Image

Concepts: Fourier Transform Kinesthetics, Nanobot Regimen, Cohobation,
Natural Order Register Machines, Product of Extremes = Product of Means,
Intelligence Through Crossing

Uses Pro model for high-quality symbolic visualizations
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from symbolic_concepts_prompts import SYMBOLIC_CONCEPTS_PROMPTS

async def main():
    print("🔬 Abstract Symbolic Concepts - PRO MODEL")
    print("=" * 70)
    print(f"Model: Gemini 3 Pro Image (gemini-3-pro-image-preview)")
    print(f"Prompts: {len(SYMBOLIC_CONCEPTS_PROMPTS)}")
    print(f"Output: examples/Symbolic Concepts/")
    print()
    print("✨ Visualizing abstract concepts through symbolic representation")
    print()

    # Output directory
    output_dir = Path(__file__).parent / "Symbolic Concepts"
    output_dir.mkdir(exist_ok=True)

    # Import GeminiClient here to avoid import errors
    from src.gemini_client import GeminiClient
    import asyncio

    # Counters
    succeeded = 0
    failed = 0
    total = len(SYMBOLIC_CONCEPTS_PROMPTS)

    # Generate with Pro model
    semaphore = asyncio.Semaphore(3)  # Slower, higher quality

    async def generate_one(prompt: str, index: int):
        async with semaphore:
            async with GeminiClient() as client:
                try:
                    # Use Pro model
                    result = await client.generate_image(prompt, model="pro")
                    return {
                        "index": index,
                        "prompt": prompt,
                        "image_data": result["image_data"],
                        "size_mb": len(result["image_data"]) / (1024 * 1024),
                        "status": "success"
                    }
                except Exception as e:
                    return {
                        "index": index,
                        "prompt": prompt,
                        "status": "error",
                        "error": str(e)
                    }

    tasks = [generate_one(p, i) for i, p in enumerate(SYMBOLIC_CONCEPTS_PROMPTS)]

    for coro in asyncio.as_completed(tasks):
        result = await coro

        if result["status"] == "success":
            # Save image
            filename = f"{result['index']:02d}_{result['prompt'][:30].replace(' ', '_').replace('/', '-')}.png"
            filepath = output_dir / filename

            with open(filepath, "wb") as f:
                f.write(result["image_data"])

            succeeded += 1
            print(f"✓ [{succeeded}/{total}] {result['size_mb']:.2f} MB - {result['prompt'][:80]}...")
            print(f"  Saved: {filepath.name}")

        else:
            failed += 1
            error_msg = result.get("error", "Unknown error")
            print(f"✗ [{failed} failures] Error: {error_msg}")

    print()
    print("=" * 70)
    print(f"📊 Symbolic Concepts Complete")
    print(f"  Total: {total}")
    print(f"  Succeeded: {succeeded} ✓")
    print(f"  Failed: {failed} ✗")
    print(f"  Success Rate: {(succeeded/total)*100:.1f}%")
    print()

    if succeeded > 0:
        print(f"✅ Symbolic concept images saved to: {output_dir.absolute()}")
        print(f"💰 Estimated cost: ${succeeded * 0.12:.2f} ({succeeded} images × $0.12)")

if __name__ == "__main__":
    asyncio.run(main())
