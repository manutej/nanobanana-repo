"""
Single Image Test - Verify API quota hypothesis

This script generates ONE image to test whether:
1. API quota has reset (allows 1 request)
2. Only first request works (code pattern bug)
3. Multi-part response fix is working correctly
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


async def single_image_test():
    """Generate a single image to test API quota and multi-part fix"""

    print("🧪 Single Image Test - API Quota Verification")
    print("=" * 60)

    # Test prompt - different from earlier tests
    test_prompt = "Sunset at the beach with palm trees and orange sky"

    print(f"Prompt: {test_prompt}")
    print(f"Time: {datetime.now(UTC).isoformat()}")
    print()

    # Initialize components
    classifier = DomainClassifier()
    template_engine = TemplateEngine()

    # Classify
    domain, confidence = classifier.classify_with_confidence(test_prompt)
    print(f"Domain: {domain} (confidence: {confidence:.2f})")

    # Enhance
    subcategory = template_engine.suggest_subcategory(test_prompt, domain)
    enhanced = template_engine.enhance(test_prompt, domain, "detailed", subcategory)
    print(f"Subcategory: {subcategory}")
    print(f"Enhanced: {enhanced[:100]}...")
    print()

    # Generate
    try:
        print("Generating image... ", end="", flush=True)

        async with GeminiClient() as client:
            result = await client.generate_image(enhanced, model="flash")

        # Save
        output_dir = Path("examples/test_images")
        output_dir.mkdir(exist_ok=True)

        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        filename = f"single_test_{timestamp}.png"
        filepath = output_dir / filename

        with open(filepath, "wb") as f:
            f.write(result["image_data"])

        size_mb = len(result["image_data"]) / (1024 * 1024)
        print(f"✅ SUCCESS")
        print()
        print("=" * 60)
        print("📊 Results")
        print(f"  File: {filepath}")
        print(f"  Size: {size_mb:.2f} MB")
        print(f"  Status: Multi-part response fix is working!")
        print()
        print("💡 Hypothesis: API quota has reset OR quota allows 1 req/period")
        print()

        return True

    except Exception as e:
        error_msg = str(e)
        print(f"❌ FAILED")
        print()
        print("=" * 60)
        print("📊 Results")
        print(f"  Error: {error_msg}")
        print()

        if "403" in error_msg or "Forbidden" in error_msg:
            print("💡 Hypothesis: API quota still exhausted (403 Forbidden)")
            print("   → Wait 24 hours for quota reset")
            print("   → OR upgrade to paid API tier")
        elif "inlineData" in error_msg:
            print("💡 Hypothesis: Multi-part response fix not working")
            print("   → This would be a critical bug!")
            print("   → But previous test succeeded, so likely not this")
        else:
            print(f"💡 Hypothesis: Different error - {error_msg}")
            print("   → Investigate this specific error")

        print()
        return False


if __name__ == "__main__":
    success = asyncio.run(single_image_test())

    if success:
        print("✨ Test passed - Ready to generate more images!")
    else:
        print("⚠️  Test failed - See error details above")
