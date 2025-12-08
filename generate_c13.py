#!/usr/bin/env python3
"""Generate C13: Context Pruning Strategies"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from src.gemini_client import GeminiClient

async def main():
    prompt_path = Path('/Users/manu/Documents/LUXOR/docs/images/context-engineering/batch-4/C13-prompt.txt')
    prompt = prompt_path.read_text()

    async with GeminiClient() as client:
        result = await client.generate_image(prompt, model="pro")
        output_path = Path('/Users/manu/Documents/LUXOR/docs/images/context-engineering/batch-4/C13-context-pruning.png')
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(result["image_data"])

        file_size_mb = len(result["image_data"]) / (1024 * 1024)
        print(f"✅ C13 generated: {file_size_mb:.2f} MB")

if __name__ == "__main__":
    asyncio.run(main())
