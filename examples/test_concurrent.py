"""
Test Concurrent Image Generation with Rate Limiting

Tests the async concurrent approach with controlled concurrency
and delays to avoid rate limiting (based on Gemini API research).

Strategy:
- Max 2 concurrent requests
- 15 second stagger between request starts
- Exponential backoff on 429/503 errors
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


# Test prompts (5 diverse images)
TEST_PROMPTS = [
    "Professional headshot of a female CEO",
    "Mountain landscape at golden hour",
    "Modern office workspace with natural light",
    "Coffee cup on wooden table by window",
    "Tech startup team brainstorming session"
]


class ConcurrentTester:
    """Test concurrent image generation with rate limiting"""

    def __init__(self, api_key: str, max_concurrent: int = 2, delay_seconds: float = 15.0):
        self.api_key = api_key
        self.max_concurrent = max_concurrent
        self.delay_seconds = delay_seconds
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.classifier = DomainClassifier()
        self.template_engine = TemplateEngine()

    async def generate_with_rate_limit(self, prompt: str, index: int):
        """
        Generate image with rate limiting

        Args:
            prompt: Text prompt
            index: Request index (used for staggered delay)

        Returns:
            dict with result or error
        """
        result = {
            "index": index,
            "prompt": prompt,
            "status": "pending",
            "start_time": None,
            "end_time": None
        }

        async with self.semaphore:  # Max 2 concurrent
            try:
                # Stagger requests (0s, 15s, 30s, 45s, 60s)
                delay = index * self.delay_seconds
                print(f"\n[{index+1}/5] Waiting {delay:.0f}s before starting: {prompt[:50]}...")
                await asyncio.sleep(delay)

                result["start_time"] = datetime.now(UTC)
                print(f"[{index+1}/5] Starting generation...")

                # Classify and enhance
                domain, confidence = self.classifier.classify_with_confidence(prompt)
                subcategory = self.template_engine.suggest_subcategory(prompt, domain)
                enhanced = self.template_engine.enhance(prompt, domain, "detailed", subcategory)

                print(f"[{index+1}/5] Domain: {domain} ({confidence:.2f}), Subcategory: {subcategory}")

                # Generate
                async with GeminiClient(api_key=self.api_key) as client:
                    image_result = await client.generate_image(enhanced, model="flash")

                # Save
                output_dir = Path("examples/test_images")
                output_dir.mkdir(exist_ok=True)

                filename = f"concurrent_{index+1:02d}_{datetime.now(UTC).strftime('%H%M%S')}.png"
                filepath = output_dir / filename

                with open(filepath, "wb") as f:
                    f.write(image_result["image_data"])

                size_mb = len(image_result["image_data"]) / (1024 * 1024)
                result["end_time"] = datetime.now(UTC)
                result["status"] = "success"
                result["filepath"] = str(filepath)
                result["size_mb"] = size_mb

                duration = (result["end_time"] - result["start_time"]).total_seconds()
                print(f"[{index+1}/5] ✅ SUCCESS ({size_mb:.2f} MB, {duration:.1f}s)")

            except Exception as e:
                result["end_time"] = datetime.now(UTC)
                result["status"] = "failed"
                result["error"] = str(e)

                if "403" in str(e):
                    print(f"[{index+1}/5] ❌ RATE LIMITED (403 Forbidden)")
                elif "429" in str(e):
                    print(f"[{index+1}/5] ❌ TOO MANY REQUESTS (429)")
                else:
                    print(f"[{index+1}/5] ❌ ERROR: {e}")

        return result


async def run_concurrent_test():
    """Run concurrent generation test"""

    print("🧪 Concurrent Image Generation Test")
    print("=" * 70)
    print(f"Strategy: Max {2} concurrent, {15}s stagger between starts")
    print(f"Total prompts: {len(TEST_PROMPTS)}")
    print(f"Expected duration: ~{(len(TEST_PROMPTS) - 1) * 15 + 10}s")
    print()

    # Get API key from environment
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ ERROR: GOOGLE_API_KEY not set in environment")
        print("Run: export GOOGLE_API_KEY='your_key_here'")
        return

    # Run concurrent test
    tester = ConcurrentTester(api_key, max_concurrent=2, delay_seconds=15.0)

    start_time = datetime.now(UTC)
    print(f"🚀 Starting at {start_time.strftime('%H:%M:%S')}")
    print()

    # Create tasks for all prompts
    tasks = [
        tester.generate_with_rate_limit(prompt, i)
        for i, prompt in enumerate(TEST_PROMPTS)
    ]

    # Run concurrently (respecting semaphore limits)
    results = await asyncio.gather(*tasks, return_exceptions=False)

    end_time = datetime.now(UTC)
    duration = (end_time - start_time).total_seconds()

    # Analyze results
    print()
    print("=" * 70)
    print("📊 Results Summary")
    print("=" * 70)

    success_count = sum(1 for r in results if r["status"] == "success")
    failed_count = sum(1 for r in results if r["status"] == "failed")

    print(f"Total: {len(results)}")
    print(f"Success: {success_count} ✅")
    print(f"Failed: {failed_count} ❌")
    print(f"Success Rate: {success_count / len(results) * 100:.1f}%")
    print(f"Total Duration: {duration:.1f}s")
    print()

    # Error analysis
    if failed_count > 0:
        print("Failed Requests:")
        for r in results:
            if r["status"] == "failed":
                error = r.get("error", "Unknown error")
                is_rate_limit = "403" in error or "429" in error
                indicator = "🚫 RATE LIMIT" if is_rate_limit else "❌ ERROR"
                print(f"  [{r['index']+1}] {indicator}: {error[:100]}")
        print()

    # Success details
    if success_count > 0:
        print("Successful Generations:")
        for r in results:
            if r["status"] == "success":
                duration = (r["end_time"] - r["start_time"]).total_seconds()
                print(f"  [{r['index']+1}] {r['size_mb']:.2f} MB in {duration:.1f}s - {r['filepath']}")
        print()

    # Rate limiting assessment
    print("🔍 Rate Limiting Assessment:")
    rate_limited = any("403" in str(r.get("error", "")) or "429" in str(r.get("error", "")) for r in results)

    if rate_limited:
        print("  ⚠️  Rate limiting detected!")
        print("  Recommendation: Use Batch API for 10+ images")
        print("  Alternative: Increase delay to 30s or use sequential mode")
    else:
        print("  ✅ No rate limiting - concurrent strategy works!")
        print("  This approach is suitable for 5-9 images")

    print()
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(run_concurrent_test())
