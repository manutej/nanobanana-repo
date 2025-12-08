#!/usr/bin/env python3
"""
Generate Philosophical-Mathematical Concepts Suite
===================================================

22 profound visualizations spanning ancient wisdom to modern science:
P01: THE UNITY (Schw

aller de Lubicz)
P02: Servus Fugitivus (Alchemical fugitive servant)
P03: Spiritus Domini (Spirit upon waters)
P04: Solve et Coagula (Alchemical transformation)
P05: Porphyrins Elixir Teacher (Light-sound molecular activation)
P06: Computational Equivalence Teacher (Wolfram's principle)
P07: Simple Programs Underlying Complexity
P08: Quark Matter & Porphyrins (Particles to life)
P09: Quantum Paradox Teacher (Superposition, observation)
P10: Φ+1 Concentration (Golden ratio convergence)
P11: Φ-1 Dispersal (Golden ratio expansion)
P12: Genesis of Φ+1 (Birth of golden mean)
P13: (√5+1)/2 (Golden ratio formula)
P14: Counting (First form of consciousness)
P15: Original Scission (Polarization of energy)
P16: Glands of Encephalon (Pineal, pituitary, hypothalamus)
P17: Numerating Action of Φ (Phi as generator)
P18: Continuous Synthesis (Discrete to continuous)
P19: Surface Limits (Form definition)
P20: First Limitation (Ternary axle system)
P21: 1:1/Φ:Φ² (Golden ratio triad)
P22: Number Line is Movement (Geometric genesis)

Model: Gemini 3 Pro Image (perfect text, high quality)
Cost: $0.12 per image × 22 = $2.64 total
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
    {"id": "P01", "title": "THE UNITY - Indivisible Cosmic Consciousness", "filename": "P01-the-unity.png"},
    {"id": "P02", "title": "Servus Fugitivus - The Fugitive Servant", "filename": "P02-servus-fugitivus.png"},
    {"id": "P03", "title": "Spiritus Domini Ferebatur Super Aquas", "filename": "P03-spiritus-domini.png"},
    {"id": "P04", "title": "Solve et Coagula", "filename": "P04-solve-et-coagula.png"},
    {"id": "P05", "title": "Porphyrins Elixir Teacher", "filename": "P05-porphyrins-elixir.png"},
    {"id": "P06", "title": "Computational Equivalence Teacher", "filename": "P06-computational-equivalence.png"},
    {"id": "P07", "title": "Simple Programs Underlying Complexity", "filename": "P07-simple-programs-complexity.png"},
    {"id": "P08", "title": "Quark Matter & Porphyrins Elixir Teacher", "filename": "P08-quark-porphyrins.png"},
    {"id": "P09", "title": "Quantum Paradox Teacher", "filename": "P09-quantum-paradox.png"},
    {"id": "P10", "title": "Φ+1 Concentration", "filename": "P10-phi-plus-1-concentration.png"},
    {"id": "P11", "title": "Φ-1 Dispersal", "filename": "P11-phi-minus-1-dispersal.png"},
    {"id": "P12", "title": "Genesis of Φ+1", "filename": "P12-genesis-phi-plus-1.png"},
    {"id": "P13", "title": "(√5+1)/2 - The Golden Ratio Formula", "filename": "P13-golden-ratio-formula.png"},
    {"id": "P14", "title": "Counting - First Innate Form of Consciousness", "filename": "P14-counting-consciousness.png"},
    {"id": "P15", "title": "The Original Scission - Polarization of Energy", "filename": "P15-original-scission.png"},
    {"id": "P16", "title": "Glands of Encephalon", "filename": "P16-glands-encephalon.png"},
    {"id": "P17", "title": "The Numerating Action of Φ", "filename": "P17-numerating-action-phi.png"},
    {"id": "P18", "title": "Continuous Synthesis", "filename": "P18-continuous-synthesis.png"},
    {"id": "P19", "title": "Surface Limits Definition of Size", "filename": "P19-surface-limits.png"},
    {"id": "P20", "title": "First Limitation - Ternary Axle System", "filename": "P20-ternary-axle-system.png"},
    {"id": "P21", "title": "1:1/Φ:Φ² - Golden Ratio Triad", "filename": "P21-golden-ratio-triad.png"},
    {"id": "P22", "title": "The Number Line Is Movement", "filename": "P22-number-line-movement.png"},
]


async def generate_all():
    """Generate all Philosophical-Mathematical concept images"""

    # Setup paths
    prompts_dir = Path(__file__).parent / "Philosophical-Mathematical Concepts"
    output_dir = prompts_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("🔮 PHILOSOPHICAL-MATHEMATICAL CONCEPTS SUITE")
    print("=" * 80)
    print()
    print("Ancient Wisdom → Modern Science → Mathematical Philosophy")
    print()
    print(f"Model: Gemini 3 Pro Image (gemini-3-pro-image-preview)")
    print(f"Concepts: {len(CONCEPTS)}")
    print(f"Expected Cost: ${len(CONCEPTS) * 0.12:.2f}")
    print()
    print("=" * 80)
    print()

    async with GeminiClient() as client:
        total_size = 0
        successful = 0
        failed = 0
        failed_list = []

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
                failed_list.append(f"{concept_id}: Prompt file missing")
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
                failed_list.append(f"{concept_id}: {str(e)[:50]}")
                print(f"    ❌ ERROR: {e}")

            print()

        # Summary
        print("=" * 80)
        print("📊 GENERATION SUMMARY")
        print("=" * 80)
        print()
        print(f"✅ Successful: {successful}/{len(CONCEPTS)}")
        print(f"❌ Failed: {failed}/{len(CONCEPTS)}")
        if failed_list:
            print("\nFailed concepts:")
            for fail in failed_list:
                print(f"  - {fail}")
        print(f"\n📦 Total Size: {total_size:.2f} MB")
        print(f"💰 Actual Cost: ${successful * 0.12:.2f}")
        print(f"📂 Output: {output_dir.relative_to(Path.cwd())}")
        print()

        if successful == len(CONCEPTS):
            print("🎉 COMPLETE SUCCESS - ALL PHILOSOPHICAL-MATHEMATICAL CONCEPTS GENERATED!")
        elif successful > 0:
            print(f"⚠️  PARTIAL SUCCESS - {successful} of {len(CONCEPTS)} generated")
        else:
            print("❌ GENERATION FAILED - No images created")

        print()
        print("=" * 80)
        print()

        # Concept guide preview
        if successful > 0:
            print("🔮 CONCEPT CATEGORIES")
            print("=" * 80)
            print()
            print("**Ancient Wisdom** (P01-P04):")
            print("  Unity, Alchemy, Genesis, Transformation")
            print()
            print("**Molecular & Quantum** (P05-P09):")
            print("  Porphyrins, Computational Equivalence, Complexity, Quantum Paradoxes")
            print()
            print("**Golden Ratio Philosophy** (P10-P13, P17, P21):")
            print("  Φ concentration/dispersal, Genesis, Formula, Numerating Action, Triad")
            print()
            print("**Consciousness & Number** (P14-P15, P18, P22):")
            print("  Counting, Scission, Synthesis, Number as Movement")
            print()
            print("**Spatial Philosophy** (P16, P19-P20):")
            print("  Glands, Surface Limits, Ternary Axle System")
            print()


if __name__ == "__main__":
    asyncio.run(generate_all())
