#!/usr/bin/env python3
"""
Generate Hermetic-Scientific Concepts Suite
============================================

6 profound visualizations bridging ancient wisdom and modern science:
- H01: THE UNITY (Schwaller de Lubicz)
- H02: Servus Fugitivus (Alchemical servant)
- H03: Spiritus Domini Ferebatur Super Aquas (Spirit upon waters)
- H04: Solve et Coagula (Alchemical transformation)
- H05: Porphyrins Elixir Teacher (Molecular light-sound activation)
- H06: Computational Equivalence Teacher (Wolfram's principle)

Model: Gemini 3 Pro Image (perfect text, high quality)
Cost: $0.12 per image × 6 = $0.72 total
Expected Success Rate: 100% (based on previous Pro model performance)
"""

import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from src.gemini_client import GeminiClient


# Concept definitions
CONCEPTS = [
    {
        "id": "H01",
        "title": "THE UNITY - Indivisible Consciousness",
        "filename": "H01-the-unity.png",
        "description": "Sacred geometry mandala expressing Schwaller de Lubicz's unity principle"
    },
    {
        "id": "H02",
        "title": "Servus Fugitivus - The Fugitive Servant",
        "filename": "H02-servus-fugitivus.png",
        "description": "Alchemical mercury - the volatile servant of transformation"
    },
    {
        "id": "H03",
        "title": "Spiritus Domini Ferebatur Super Aquas",
        "filename": "H03-spiritus-domini.png",
        "description": "Divine spirit moving upon primordial waters - Genesis visualization"
    },
    {
        "id": "H04",
        "title": "Solve et Coagula",
        "filename": "H04-solve-et-coagula.png",
        "description": "Alchemical cycle of dissolution and coagulation"
    },
    {
        "id": "H05",
        "title": "Porphyrins Elixir Teacher",
        "filename": "H05-porphyrins-elixir.png",
        "description": "Molecular wisdom - light and sound activation of life's core structure"
    },
    {
        "id": "H06",
        "title": "Computational Equivalence Teacher",
        "filename": "H06-computational-equivalence.png",
        "description": "Wolfram's principle - simple rules reaching universal complexity"
    }
]


async def generate_all():
    """Generate all Hermetic-Scientific concept images"""

    # Setup paths
    prompts_dir = Path(__file__).parent / "Hermetic-Scientific Concepts"
    output_dir = prompts_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("🔮 HERMETIC-SCIENTIFIC CONCEPTS SUITE")
    print("=" * 70)
    print()
    print("Ancient Wisdom ∩ Modern Science")
    print()
    print(f"Model: Gemini 3 Pro Image (gemini-3-pro-image-preview)")
    print(f"Concepts: {len(CONCEPTS)}")
    print(f"Expected Cost: ${len(CONCEPTS) * 0.12:.2f}")
    print()
    print("=" * 70)
    print()

    async with GeminiClient() as client:
        total_size = 0
        successful = 0
        failed = 0

        for i, concept in enumerate(CONCEPTS, 1):
            concept_id = concept["id"]
            title = concept["title"]
            filename = concept["filename"]

            print(f"[{i}/{len(CONCEPTS)}] Generating: {title}")
            print(f"    ID: {concept_id}")

            # Read prompt
            prompt_file = prompts_dir / f"{concept_id}-prompt.txt"
            if not prompt_file.exists():
                print(f"    ❌ ERROR: Prompt file not found: {prompt_file}")
                failed += 1
                print()
                continue

            prompt = prompt_file.read_text()

            # Generate image
            try:
                result = await client.generate_image(prompt, model="pro")

                # Save image
                output_path = output_dir / filename
                with open(output_path, 'wb') as f:
                    f.write(result["image_data"])

                size_mb = len(result["image_data"]) / (1024 * 1024)
                total_size += size_mb
                successful += 1

                print(f"    ✅ Success! {size_mb:.2f} MB")
                print(f"    📁 {output_path.relative_to(Path.cwd())}")

            except Exception as e:
                failed += 1
                print(f"    ❌ ERROR: {e}")

            print()

        # Summary
        print("=" * 70)
        print("📊 GENERATION SUMMARY")
        print("=" * 70)
        print()
        print(f"✅ Successful: {successful}/{len(CONCEPTS)}")
        print(f"❌ Failed: {failed}/{len(CONCEPTS)}")
        print(f"📦 Total Size: {total_size:.2f} MB")
        print(f"💰 Actual Cost: ${successful * 0.12:.2f}")
        print(f"📂 Output: {output_dir.relative_to(Path.cwd())}")
        print()

        if successful == len(CONCEPTS):
            print("🎉 COMPLETE SUCCESS - ALL HERMETIC-SCIENTIFIC CONCEPTS GENERATED!")
        elif successful > 0:
            print(f"⚠️  PARTIAL SUCCESS - {successful} of {len(CONCEPTS)} generated")
        else:
            print("❌ GENERATION FAILED - No images created")

        print()
        print("=" * 70)
        print()

        # Concept guide
        if successful > 0:
            print("🔮 HERMETIC-SCIENTIFIC CONCEPTS GUIDE")
            print("=" * 70)
            print()
            for concept in CONCEPTS:
                print(f"**{concept['title']}**")
                print(f"  {concept['description']}")
                print()


if __name__ == "__main__":
    asyncio.run(generate_all())
