#!/usr/bin/env python3
"""
Generate Context Engineering images using async batch pipeline

Tests the full pipeline:
1. Deep research → prompts extracted
2. Async batch generation
3. Organized output in 'Context Engineering' folder
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import from src/
sys.path.insert(0, str(Path(__file__).parent.parent))

from context_engineering_prompts import CONTEXT_ENGINEERING_PROMPTS
from simple_batch import generate_batch_streaming

async def main():
    print("🎨 Context Engineering Image Generation")
    print("=" * 70)
    print(f"Prompts: {len(CONTEXT_ENGINEERING_PROMPTS)}")
    print(f"Output: examples/Context Engineering/")
    print()

    # Output directory
    output_dir = Path(__file__).parent / "Context Engineering"
    output_dir.mkdir(exist_ok=True)

    # Counters
    succeeded = 0
    failed = 0
    total = len(CONTEXT_ENGINEERING_PROMPTS)

    # Generate images using async streaming
    async for result in generate_batch_streaming(
        CONTEXT_ENGINEERING_PROMPTS,
        max_concurrent=5
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
    print(f"📊 Batch Complete")
    print(f"  Total: {total}")
    print(f"  Succeeded: {succeeded} ✓")
    print(f"  Failed: {failed} ✗")
    print(f"  Success Rate: {(succeeded/total)*100:.1f}%")
    print()

    if succeeded > 0:
        print(f"✅ Images saved to: {output_dir.absolute()}")

if __name__ == "__main__":
    asyncio.run(main())
