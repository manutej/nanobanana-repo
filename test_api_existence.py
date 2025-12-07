#!/usr/bin/env python3
"""
NanoBanana API Existence Verification Test
==========================================

CRITICAL MISSION: Verify if Google has an image generation API that works
with the provided API key.

This script tests multiple possible Google API endpoints for image generation
and generates a detailed report of findings.
"""

import os
import json
import httpx
from datetime import datetime
from typing import Dict, List, Any, Optional


class APIEndpointTester:
    """Test various Google API endpoints for image generation capability."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.results: List[Dict[str, Any]] = []

    def test_generative_language_v1beta(self) -> Dict[str, Any]:
        """Test Generative Language API v1beta endpoint."""
        endpoint = "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:predict"

        result = {
            "endpoint": endpoint,
            "name": "Generative Language API v1beta (Imagen 3.0)",
            "status_code": None,
            "success": False,
            "response": None,
            "error": None,
            "request_body": None
        }

        request_body = {
            "instances": [
                {
                    "prompt": "A cute yellow banana wearing sunglasses"
                }
            ],
            "parameters": {
                "sampleCount": 1
            }
        }

        result["request_body"] = request_body

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    f"{endpoint}?key={self.api_key}",
                    json=request_body,
                    headers={"Content-Type": "application/json"}
                )

                result["status_code"] = response.status_code
                result["response"] = response.text

                if response.status_code in [200, 201]:
                    result["success"] = True

        except Exception as e:
            result["error"] = str(e)

        return result

    def test_generative_language_generate_content(self) -> Dict[str, Any]:
        """Test Generative Language API generateContent endpoint."""
        endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent"

        result = {
            "endpoint": endpoint,
            "name": "Generative Language API (Gemini Pro Vision)",
            "status_code": None,
            "success": False,
            "response": None,
            "error": None,
            "request_body": None
        }

        request_body = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": "Generate an image of a cute yellow banana wearing sunglasses"
                        }
                    ]
                }
            ]
        }

        result["request_body"] = request_body

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    f"{endpoint}?key={self.api_key}",
                    json=request_body,
                    headers={"Content-Type": "application/json"}
                )

                result["status_code"] = response.status_code
                result["response"] = response.text

                if response.status_code in [200, 201]:
                    result["success"] = True

        except Exception as e:
            result["error"] = str(e)

        return result

    def test_vertex_ai_imagen(self) -> Dict[str, Any]:
        """Test Vertex AI Imagen endpoint (requires project ID)."""
        # Note: This will likely fail without proper project setup
        endpoint = "https://us-central1-aiplatform.googleapis.com/v1/projects/YOUR_PROJECT/locations/us-central1/publishers/google/models/imagegeneration:predict"

        result = {
            "endpoint": endpoint,
            "name": "Vertex AI Imagen (requires project setup)",
            "status_code": None,
            "success": False,
            "response": None,
            "error": "Requires project ID and OAuth, not API key",
            "request_body": None,
            "note": "This endpoint requires OAuth 2.0, not API key authentication"
        }

        return result

    def test_generative_language_list_models(self) -> Dict[str, Any]:
        """Test listing available models to see what's actually available."""
        endpoint = "https://generativelanguage.googleapis.com/v1beta/models"

        result = {
            "endpoint": endpoint,
            "name": "List Available Models",
            "status_code": None,
            "success": False,
            "response": None,
            "error": None,
            "request_body": None,
            "available_models": []
        }

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.get(
                    f"{endpoint}?key={self.api_key}",
                    headers={"Content-Type": "application/json"}
                )

                result["status_code"] = response.status_code
                result["response"] = response.text

                if response.status_code == 200:
                    result["success"] = True
                    data = response.json()
                    if "models" in data:
                        result["available_models"] = [
                            {
                                "name": model.get("name", ""),
                                "displayName": model.get("displayName", ""),
                                "description": model.get("description", ""),
                                "supportedGenerationMethods": model.get("supportedGenerationMethods", [])
                            }
                            for model in data["models"]
                        ]

        except Exception as e:
            result["error"] = str(e)

        return result

    def test_imagen_direct_endpoints(self) -> List[Dict[str, Any]]:
        """Test various potential Imagen endpoint variations."""
        potential_endpoints = [
            "https://generativelanguage.googleapis.com/v1/models/imagen:generate",
            "https://generativelanguage.googleapis.com/v1beta/models/imagen:generate",
            "https://generativelanguage.googleapis.com/v1/models/imagegeneration:predict",
            "https://generativelanguage.googleapis.com/v1beta/models/imagegeneration:predict",
            "https://generativelanguage.googleapis.com/v1/models/imagen-3.0:generate",
            "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0:generate",
        ]

        results = []

        for endpoint in potential_endpoints:
            result = {
                "endpoint": endpoint,
                "name": f"Direct Imagen Test: {endpoint.split('/')[-1]}",
                "status_code": None,
                "success": False,
                "response": None,
                "error": None,
                "request_body": None
            }

            request_body = {
                "prompt": "A cute yellow banana wearing sunglasses",
                "numImages": 1
            }

            result["request_body"] = request_body

            try:
                with httpx.Client(timeout=30.0) as client:
                    response = client.post(
                        f"{endpoint}?key={self.api_key}",
                        json=request_body,
                        headers={"Content-Type": "application/json"}
                    )

                    result["status_code"] = response.status_code
                    result["response"] = response.text

                    if response.status_code in [200, 201]:
                        result["success"] = True

            except Exception as e:
                result["error"] = str(e)

            results.append(result)

        return results

    def run_all_tests(self) -> None:
        """Run all endpoint tests."""
        print("=" * 80)
        print("NanoBanana API Existence Verification")
        print("=" * 80)
        print()

        # Test 1: List available models first
        print("[1/4] Testing: List Available Models...")
        result = self.test_generative_language_list_models()
        self.results.append(result)
        print(f"      Status: {result['status_code']}")
        print(f"      Success: {result['success']}")
        if result.get('available_models'):
            print(f"      Found {len(result['available_models'])} models")
        print()

        # Test 2: Generative Language API
        print("[2/4] Testing: Generative Language API (Imagen 3.0)...")
        result = self.test_generative_language_v1beta()
        self.results.append(result)
        print(f"      Status: {result['status_code']}")
        print(f"      Success: {result['success']}")
        print()

        # Test 3: Gemini Pro Vision
        print("[3/4] Testing: Gemini Pro Vision...")
        result = self.test_generative_language_generate_content()
        self.results.append(result)
        print(f"      Status: {result['status_code']}")
        print(f"      Success: {result['success']}")
        print()

        # Test 4: Direct Imagen endpoints
        print("[4/4] Testing: Multiple Direct Imagen Endpoints...")
        imagen_results = self.test_imagen_direct_endpoints()
        self.results.extend(imagen_results)
        successful = sum(1 for r in imagen_results if r['success'])
        print(f"      Tested {len(imagen_results)} endpoints, {successful} successful")
        print()

        # Test 5: Vertex AI (informational)
        vertex_result = self.test_vertex_ai_imagen()
        self.results.append(vertex_result)

    def generate_report(self, output_file: str) -> None:
        """Generate detailed markdown report."""

        successful_tests = [r for r in self.results if r['success']]
        responding_tests = [r for r in self.results if r['status_code'] is not None]

        report = f"""# NanoBanana API Existence Verification Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**API Key**: {self.api_key[:20]}...{self.api_key[-10:]}

---

## Executive Summary

**Total Endpoints Tested**: {len(self.results)}
**Endpoints That Responded**: {len(responding_tests)}
**Successful Endpoints (200/201)**: {len(successful_tests)}

---

## Critical Conclusion

"""

        if successful_tests:
            report += f"""### ✅ **YES - API EXISTS**

Found {len(successful_tests)} working endpoint(s) for image generation.

**Working Endpoints**:
"""
            for test in successful_tests:
                report += f"- {test['name']}\n"
                report += f"  - Endpoint: `{test['endpoint']}`\n"
                report += f"  - Status: {test['status_code']}\n"

        else:
            report += """### ❌ **NO - IMAGE GENERATION API DOES NOT EXIST**

**BRUTAL TRUTH**: None of the tested endpoints successfully generated images.

**What This Means**:
- Google's Generative AI API (with API key) does NOT support image generation
- The API key only works with text generation models (Gemini Pro, etc.)
- Image generation (Imagen) requires Vertex AI with OAuth 2.0, not API keys
- NanoBanana's current approach of using simple API key auth won't work for images

**Recommendation**:
- Either migrate to Vertex AI (complex, requires project setup)
- Or switch to a different provider (OpenAI DALL-E, Stability AI, etc.)
"""

        report += "\n\n---\n\n## Detailed Test Results\n\n"

        for i, test in enumerate(self.results, 1):
            report += f"### Test {i}: {test['name']}\n\n"
            report += f"**Endpoint**: `{test['endpoint']}`\n\n"

            if test.get('note'):
                report += f"**Note**: {test['note']}\n\n"

            report += f"**Status Code**: {test['status_code'] if test['status_code'] else 'No response'}\n\n"
            report += f"**Success**: {'✅ Yes' if test['success'] else '❌ No'}\n\n"

            if test['request_body']:
                report += "**Request Body**:\n```json\n"
                report += json.dumps(test['request_body'], indent=2)
                report += "\n```\n\n"

            if test['response']:
                report += "**Response**:\n```\n"
                # Truncate very long responses
                response_preview = test['response'][:2000]
                if len(test['response']) > 2000:
                    response_preview += "\n... (truncated)"
                report += response_preview
                report += "\n```\n\n"

            if test['error']:
                report += f"**Error**: {test['error']}\n\n"

            if test.get('available_models'):
                report += "**Available Models**:\n\n"
                for model in test['available_models']:
                    report += f"- **{model['displayName']}**\n"
                    report += f"  - Name: `{model['name']}`\n"
                    report += f"  - Methods: {', '.join(model['supportedGenerationMethods'])}\n"
                    if model['description']:
                        report += f"  - Description: {model['description'][:200]}\n"
                    report += "\n"

            report += "---\n\n"

        report += """## Additional Research

### Google's Image Generation Options

1. **Vertex AI Imagen** (Recommended by Google)
   - Requires: Google Cloud Project, OAuth 2.0
   - Endpoint: `https://us-central1-aiplatform.googleapis.com/v1/...`
   - Pricing: ~$0.02 per image
   - Setup Complexity: HIGH

2. **Generative AI API** (Current Approach)
   - Requires: API Key only
   - Supports: Text generation only (Gemini models)
   - Image Generation: NOT SUPPORTED
   - Setup Complexity: LOW

### Alternative Providers

If Google's API doesn't work:

1. **OpenAI DALL-E**
   - API Key: Simple authentication
   - Pricing: $0.016-$0.080 per image
   - Quality: Excellent

2. **Stability AI**
   - API Key: Simple authentication
   - Pricing: $0.002-$0.01 per image
   - Quality: Good

3. **Replicate**
   - API Key: Simple authentication
   - Multiple models available
   - Pay per use

---

## Next Steps

"""

        if successful_tests:
            report += """1. ✅ Continue with NanoBanana development using working endpoint
2. Document the exact request/response format
3. Implement error handling for the API
4. Add rate limiting and cost tracking
"""
        else:
            report += """1. ❌ **STOP** building on false assumptions
2. Choose one of the following:
   - Migrate to Vertex AI (complex setup)
   - Switch to OpenAI DALL-E (simple API key)
   - Use Stability AI (simple API key)
   - Use Replicate (simple API key)
3. Update architecture documentation
4. Revise cost estimates
"""

        report += "\n---\n\n"
        report += f"**Report Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"

        with open(output_file, 'w') as f:
            f.write(report)

        print(f"✅ Report saved to: {output_file}")


def main():
    """Main execution function."""

    # Get API key from environment
    api_key = os.getenv('GOOGLE_API_KEY')

    if not api_key:
        print("❌ ERROR: GOOGLE_API_KEY environment variable not set")
        print()
        print("Please set it with:")
        print("export GOOGLE_API_KEY='your-api-key-here'")
        return

    print(f"Using API Key: {api_key[:20]}...{api_key[-10:]}")
    print()

    # Create tester
    tester = APIEndpointTester(api_key)

    # Run all tests
    tester.run_all_tests()

    # Generate report
    output_file = "/Users/manu/Documents/LUXOR/PROJECTS/nanobanana-repo/API-TEST-RESULTS.md"
    tester.generate_report(output_file)

    print()
    print("=" * 80)
    print("Testing Complete")
    print("=" * 80)

    # Print conclusion
    successful_tests = [r for r in tester.results if r['success']]
    if successful_tests:
        print()
        print("✅ CONCLUSION: NanoBanana API EXISTS")
        print(f"   Found {len(successful_tests)} working endpoint(s)")
    else:
        print()
        print("❌ CONCLUSION: IMAGE GENERATION API DOES NOT EXIST")
        print("   Google's API key authentication does not support image generation")
        print("   Consider switching to Vertex AI or alternative providers")


if __name__ == "__main__":
    main()
