"""
Generate 10 Example Images - NanoBanana Showcase

This script generates 10 diverse images showcasing all domains and subcategories.
Each example demonstrates the template enhancement in action.
"""

import asyncio
import json
import os
import sys
from datetime import datetime, UTC
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from domain_classifier import DomainClassifier
from template_engine import TemplateEngine
from gemini_client import GeminiClient


# 10 Example Prompts (from EXAMPLE-PROMPTS.md)
EXAMPLES = [
    {
        "id": 1,
        "name": "corporate_portrait",
        "prompt": "Professional headshot of a female CEO in her 40s",
        "quality": "expert",
        "description": "Corporate portrait showcasing professional photography template"
    },
    {
        "id": 2,
        "name": "mountain_sunset",
        "prompt": "Sunset over mountains with a lake in foreground",
        "quality": "expert",
        "description": "Dramatic landscape with golden hour lighting"
    },
    {
        "id": 3,
        "name": "wireless_headphones",
        "prompt": "Wireless headphones for Amazon listing",
        "quality": "expert",
        "description": "E-commerce product photography with white background"
    },
    {
        "id": 4,
        "name": "impressionist_garden",
        "prompt": "Garden with flowers in impressionist style",
        "quality": "expert",
        "description": "Impressionist painting in Monet style"
    },
    {
        "id": 5,
        "name": "microservices_diagram",
        "prompt": "Cloud-native microservices architecture for image generation API with Cloud Run, Firestore, and Cloud Storage",
        "quality": "expert",
        "description": "Technical architecture diagram with color-coded components"
    },
    {
        "id": 6,
        "name": "oauth_flowchart",
        "prompt": "User authentication flow with OAuth2 and error handling",
        "quality": "detailed",
        "description": "Process flowchart with BPMN notation"
    },
    {
        "id": 7,
        "name": "mobile_wireframe",
        "prompt": "Mobile app wireframe for image generation interface with prompt input and gallery",
        "quality": "expert",
        "description": "High-fidelity UX wireframe following Material Design"
    },
    {
        "id": 8,
        "name": "futuristic_car",
        "prompt": "Futuristic sports car in a studio environment",
        "quality": "expert",
        "description": "Photorealistic 3D render with PBR materials"
    },
    {
        "id": 9,
        "name": "coffee_lifestyle",
        "prompt": "Coffee mug being held while reading a book by a window",
        "quality": "expert",
        "description": "Lifestyle product photography with natural lighting"
    },
    {
        "id": 10,
        "name": "nanobanana_architecture",
        "prompt": "NanoBanana image generation microservice architecture showing Flask API, domain classifier, template engine, Gemini API client, Cloud Run deployment, and data flow from user request to generated image",
        "quality": "expert",
        "description": "META: The microservice diagramming itself!"
    }
]


async def generate_all_examples():
    """Generate all 10 example images"""

    # Create output directory
    output_dir = Path(__file__).parent / "images"
    output_dir.mkdir(exist_ok=True)

    # Initialize components
    classifier = DomainClassifier()
    template_engine = TemplateEngine()

    # Track results
    results = []

    print("🍌 NanoBanana Example Generation")
    print("=" * 50)
    print(f"Generating 10 diverse examples...")
    print(f"Output directory: {output_dir}")
    print()

    async with GeminiClient() as client:
        for example in EXAMPLES:
            print(f"Example {example['id']}/10: {example['name']}")
            print(f"  Prompt: {example['prompt'][:60]}...")

            try:
                # Step 1: Classify domain
                domain, confidence = classifier.classify_with_confidence(example['prompt'])
                print(f"  Domain: {domain} (confidence: {confidence:.2f})")

                # Step 2: Suggest subcategory
                subcategory = template_engine.suggest_subcategory(example['prompt'], domain)
                print(f"  Subcategory: {subcategory}")

                # Step 3: Enhance prompt
                enhanced = template_engine.enhance(
                    example['prompt'],
                    domain=domain,
                    quality=example['quality'],
                    subcategory=subcategory
                )
                print(f"  Enhanced: {enhanced[:80]}...")

                # Step 4: Generate image
                print(f"  Generating image... (this may take ~3 seconds)")
                result = await client.generate_image(enhanced, model="flash")

                # Step 5: Save image
                filename = f"{example['id']:02d}_{example['name']}.png"
                filepath = output_dir / filename
                with open(filepath, "wb") as f:
                    f.write(result["image_data"])

                file_size = len(result["image_data"]) / 1024 / 1024  # MB
                print(f"  ✓ Saved: {filename} ({file_size:.2f} MB)")

                # Track metadata
                results.append({
                    "id": example['id'],
                    "name": example['name'],
                    "filename": filename,
                    "description": example['description'],
                    "original_prompt": example['prompt'],
                    "enhanced_prompt": enhanced,
                    "domain": domain,
                    "subcategory": subcategory,
                    "quality": example['quality'],
                    "confidence": confidence,
                    "file_size_mb": round(file_size, 2),
                    "model": "flash",
                    "generated_at": datetime.now(UTC).isoformat()
                })

                print()

            except Exception as e:
                print(f"  ✗ Error: {e}")
                print()
                continue

    # Save metadata
    metadata_file = output_dir / "metadata.json"
    with open(metadata_file, "w") as f:
        json.dump({
            "examples": results,
            "total_count": len(results),
            "generated_at": datetime.now(UTC).isoformat(),
            "total_cost_usd": len(results) * 0.039  # Flash model cost
        }, f, indent=2)

    print("=" * 50)
    print(f"✅ Generated {len(results)}/10 examples")
    print(f"💰 Total cost: ${len(results) * 0.039:.2f}")
    print(f"📊 Metadata: {metadata_file}")
    print()

    # Print summary
    print("Summary:")
    for result in results:
        print(f"  {result['id']:2d}. {result['name']:30s} - {result['domain']:12s}/{result['subcategory']:15s} ({result['file_size_mb']:.1f} MB)")


if __name__ == "__main__":
    asyncio.run(generate_all_examples())
