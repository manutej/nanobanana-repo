"""
Quick batch test - 5 diverse prompts to validate multi-part response fix
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import asyncio
from pathlib import Path
from datetime import datetime, UTC
from gemini_client import GeminiClient
from domain_classifier import DomainClassifier
from template_engine import TemplateEngine


# 5 diverse test prompts covering different domains
BATCH_1 = [
    {
        "name": "headshot",
        "prompt": "Professional headshot of a software engineer",
        "expected_domain": "photography"
    },
    {
        "name": "landscape",
        "prompt": "Mountain sunset with lake reflection",
        "expected_domain": "photography"
    },
    {
        "name": "architecture_diagram",
        "prompt": "Microservices architecture with API gateway",
        "expected_domain": "diagrams"
    },
    {
        "name": "product_photo",
        "prompt": "Wireless keyboard on desk for Amazon listing",
        "expected_domain": "photography"
    },
    {
        "name": "flowchart",
        "prompt": "User authentication flow with OAuth2",
        "expected_domain": "diagrams"
    }
]


async def run_batch_test(batch_name: str, prompts: list):
    """Run batch test with comprehensive error handling"""

    print(f"🧪 Running {batch_name}")
    print("=" * 60)

    # Initialize components
    classifier = DomainClassifier()
    template_engine = TemplateEngine()

    # Output directory
    output_dir = Path("examples/test_images")
    output_dir.mkdir(exist_ok=True)

    results = {
        "batch": batch_name,
        "started_at": datetime.now(UTC).isoformat(),
        "tests": [],
        "summary": {
            "total": len(prompts),
            "passed": 0,
            "failed": 0
        }
    }

    async with GeminiClient() as client:
        for idx, test in enumerate(prompts, 1):
            print(f"\nTest {idx}/{len(prompts)}: {test['name']}")
            print(f"  Prompt: {test['prompt']}")

            test_result = {
                "name": test["name"],
                "prompt": test["prompt"],
                "expected_domain": test.get("expected_domain"),
                "status": "pending"
            }

            try:
                # Classify
                domain, confidence = classifier.classify_with_confidence(test["prompt"])
                print(f"  Domain: {domain} (confidence: {confidence:.2f})")
                test_result["domain"] = domain
                test_result["confidence"] = confidence

                # Suggest subcategory
                subcategory = template_engine.suggest_subcategory(test["prompt"], domain)
                print(f"  Subcategory: {subcategory}")
                test_result["subcategory"] = subcategory

                # Enhance
                enhanced = template_engine.enhance(
                    test["prompt"],
                    domain,
                    quality="detailed",
                    subcategory=subcategory
                )
                print(f"  Enhanced: {enhanced[:80]}...")
                test_result["enhanced_prompt"] = enhanced

                # Generate
                print(f"  Generating... ", end="", flush=True)
                result = await client.generate_image(enhanced, model="flash")

                # Save
                filename = f"{idx:02d}_{test['name']}.png"
                filepath = output_dir / filename
                with open(filepath, "wb") as f:
                    f.write(result["image_data"])

                size_mb = len(result["image_data"]) / (1024 * 1024)
                print(f"✅ Saved ({size_mb:.2f} MB)")

                test_result["status"] = "passed"
                test_result["output_file"] = str(filepath)
                test_result["size_bytes"] = len(result["image_data"])
                results["summary"]["passed"] += 1

            except Exception as e:
                print(f"❌ Error: {e}")
                test_result["status"] = "failed"
                test_result["error"] = str(e)
                results["summary"]["failed"] += 1

            results["tests"].append(test_result)

    # Print summary
    print("\n" + "=" * 60)
    print(f"📊 {batch_name} Summary")
    print(f"  Total: {results['summary']['total']}")
    print(f"  Passed: {results['summary']['passed']} ✅")
    print(f"  Failed: {results['summary']['failed']} ❌")
    print(f"  Success Rate: {results['summary']['passed'] / results['summary']['total'] * 100:.1f}%")

    return results


async def main():
    """Run batch test"""
    results = await run_batch_test("Batch 1 - Diverse Prompts", BATCH_1)

    # Expected: 5/5 success if multi-part response fix is working
    if results["summary"]["failed"] > 0:
        print("\n⚠️  Some tests failed - investigating...")
        for test in results["tests"]:
            if test["status"] == "failed":
                print(f"  - {test['name']}: {test.get('error', 'Unknown error')}")
    else:
        print("\n✨ All tests passed! Multi-part response fix is working.")


if __name__ == "__main__":
    asyncio.run(main())
