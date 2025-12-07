#!/usr/bin/env python3
"""Generate advanced complexity examples (11-15 only for demo)."""

import asyncio
import json
import os
import sys
from datetime import datetime, UTC
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from domain_classifier import DomainClassifier
from template_engine import TemplateEngine
from gemini_client import GeminiClient

ADVANCED_EXAMPLES = [
    {
        "id": 11,
        "name": "food_photography",
        "prompt": "Gourmet pasta carbonara being twirled on a fork with steam rising, captured mid-action with dramatic side lighting and shallow depth of field, professional food photography for Michelin restaurant menu",
        "quality": "expert",
        "description": "Cinematic food photography with motion and steam"
    },
    {
        "id": 12,
        "name": "kubernetes_gitops",
        "prompt": "Kubernetes multi-cluster deployment architecture showing GitOps workflow with ArgoCD, Flux, and Helm, including staging and production environments, automated rollbacks, and progressive delivery",
        "quality": "expert",
        "description": "Complex K8s architecture with GitOps"
    },
    {
        "id": 13,
        "name": "brutalist_architecture",
        "prompt": "Brutalist concrete building photographed from low angle with strong geometric shapes and dramatic shadows, high-contrast black and white fine art architectural photography",
        "quality": "expert",
        "description": "Architectural photography with geometric emphasis"
    },
    {
        "id": 14,
        "name": "event_driven_sequence",
        "prompt": "Event-driven microservices sequence diagram showing order placement flow with EventBridge, Order Service, Inventory Service, Payment Service, and Notification Service with retry logic and dead-letter queues",
        "quality": "expert",
        "description": "Complex sequence diagram with async messaging"
    },
    {
        "id": 15,
        "name": "cyberpunk_street",
        "prompt": "Cyberpunk street scene at night with neon signs in Japanese and English, rain-slicked streets reflecting colorful lights, figure in hooded jacket, Blade Runner aesthetic, digital painting",
        "quality": "expert",
        "description": "Cinematic cyberpunk digital art"
    }
]

async def main():
    print("🍌 NanoBanana Advanced Examples Generation")
    print("=" * 50)
    print("Generating 5 advanced complexity examples...")
    print(f"Output directory: {Path.cwd() / 'examples' / 'images'}\n")

    classifier = DomainClassifier()
    template_engine = TemplateEngine()
    results = []

    async with GeminiClient() as client:
        for i, example in enumerate(ADVANCED_EXAMPLES, 1):
            print(f"Example {i}/5: {example['name']}")
            print(f"  Prompt: {example['prompt'][:60]}...")

            domain, confidence = classifier.classify_with_confidence(example['prompt'])
            print(f"  Domain: {domain} (confidence: {confidence:.2f})")

            subcategory = template_engine.suggest_subcategory(example['prompt'], domain)
            print(f"  Subcategory: {subcategory}")

            enhanced = template_engine.enhance(
                example['prompt'],
                domain,
                example['quality'],
                subcategory
            )
            print(f"  Enhanced: {enhanced[:60]}...")

            print(f"  Generating image... (this may take ~3 seconds)")

            try:
                result = await client.generate_image(enhanced, model="flash")

                filename = f"{example['id']:02d}_{example['name']}.png"
                filepath = Path.cwd() / "examples" / "images" / filename

                with open(filepath, "wb") as f:
                    f.write(result["image_data"])

                file_size = len(result["image_data"]) / (1024 * 1024)
                print(f"  ✓ Saved: {filename} ({file_size:.2f} MB)\n")

                results.append({
                    "id": example["id"],
                    "name": example["name"],
                    "filename": filename,
                    "description": example["description"],
                    "original_prompt": example["prompt"],
                    "enhanced_prompt": enhanced,
                    "domain": domain,
                    "subcategory": subcategory,
                    "quality": example["quality"],
                    "confidence": confidence,
                    "file_size_mb": round(file_size, 2),
                    "model": "flash",
                    "generated_at": datetime.now(UTC).isoformat()
                })

            except Exception as e:
                print(f"  ✗ Error: {e}\n")

    # Save metadata
    metadata_file = Path.cwd() / "examples" / "images" / "advanced_metadata.json"
    with open(metadata_file, "w") as f:
        json.dump({
            "examples": results,
            "total_count": len(results),
            "generated_at": datetime.now(UTC).isoformat(),
            "total_cost_usd": len(results) * 0.039
        }, f, indent=2)

    print("=" * 50)
    print(f"✅ Generated {len(results)}/5 examples")
    print(f"💰 Total cost: ${len(results) * 0.039:.2f}")
    print(f"📊 Metadata: {metadata_file}")
    print("\nSummary:")
    for r in results:
        print(f"  {r['id']:2d}. {r['name']:25s} - {r['domain']:12s}/{r['subcategory']:15s} ({r['file_size_mb']:.1f} MB)")

if __name__ == "__main__":
    asyncio.run(main())
