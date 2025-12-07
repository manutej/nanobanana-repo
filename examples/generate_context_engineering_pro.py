#!/usr/bin/env python3
"""
Generate Context Engineering images using Gemini 3 Pro Image (higher quality)

Uses refined prompts optimized for accurate text rendering and clarity.
Model: gemini-3-pro-image-preview (state-of-the-art text rendering)
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import from src/
sys.path.insert(0, str(Path(__file__).parent.parent))

from context_engineering_prompts_pro import CONTEXT_ENGINEERING_PROMPTS_PRO
from simple_batch import generate_batch_streaming

async def main():
    print("🎨 Context Engineering Image Generation - PRO MODEL")
    print("=" * 70)
    print(f"Model: Gemini 3 Pro Image (gemini-3-pro-image-preview)")
    print(f"Prompts: {len(CONTEXT_ENGINEERING_PROMPTS_PRO)}")
    print(f"Output: examples/Context Engineering Pro/")
    print()
    print("✨ Using refined prompts with explicit text rendering requirements")
    print("✨ State-of-the-art quality for technical diagrams")
    print()

    # Output directory
    output_dir = Path(__file__).parent / "Context Engineering Pro"
    output_dir.mkdir(exist_ok=True)

    # Counters
    succeeded = 0
    failed = 0
    total = len(CONTEXT_ENGINEERING_PROMPTS_PRO)

    # Modified generator to use PRO model
    async def generate_with_pro_model(prompts, max_concurrent=5):
        """Generate using Pro model instead of Flash"""
        from src.gemini_client import GeminiClient
        import asyncio

        semaphore = asyncio.Semaphore(max_concurrent)

        async def generate_one(prompt: str, index: int):
            async with semaphore:
                async with GeminiClient() as client:
                    try:
                        # Use "pro" model for higher quality
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

        tasks = [generate_one(p, i) for i, p in enumerate(prompts)]

        for coro in asyncio.as_completed(tasks):
            yield await coro

    # Generate images using PRO model
    async for result in generate_with_pro_model(
        CONTEXT_ENGINEERING_PROMPTS_PRO,
        max_concurrent=3  # Slower but higher quality
    ):
        if result["status"] == "success":
            # Save image with descriptive filename
            filename = f"{result['index']:02d}_{result['prompt'][:30].replace(' ', '_')}.png"
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
    print(f"📊 PRO Model Batch Complete")
    print(f"  Total: {total}")
    print(f"  Succeeded: {succeeded} ✓")
    print(f"  Failed: {failed} ✗")
    print(f"  Success Rate: {(succeeded/total)*100:.1f}%")
    print()

    if succeeded > 0:
        print(f"✅ High-quality images saved to: {output_dir.absolute()}")
        print(f"💰 Estimated cost: ${succeeded * 0.12:.2f} ({succeeded} images × $0.12)")

if __name__ == "__main__":
    asyncio.run(main())
