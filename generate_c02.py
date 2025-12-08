#!/usr/bin/env python3
"""Generate C02: 7-Layer Context Stack"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.gemini_client import GeminiClient

async def main():
    # Read prompt
    prompt_path = Path('/Users/manu/Documents/LUXOR/docs/images/context-engineering/batch-2/C02-prompt.txt')
    prompt = prompt_path.read_text()

    print("🎨 Generating C02: 7-Layer Context Stack")
    print("Model: Gemini 3 Pro Image (gemini-3-pro-image-preview)")
    print()

    async with GeminiClient() as client:
        try:
            result = await client.generate_image(prompt, model="pro")

            # Save image
            output_path = Path('/Users/manu/Documents/LUXOR/docs/images/context-engineering/batch-2/C02-7-layer-stack.png')
            with open(output_path, 'wb') as f:
                f.write(result["image_data"])

            size_mb = len(result["image_data"]) / (1024 * 1024)
            print(f"✅ Success! Image saved ({size_mb:.2f} MB)")
            print(f"📁 {output_path}")

        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
