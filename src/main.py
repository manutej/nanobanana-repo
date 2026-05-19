"""
NanoBanana Image Generation Service - Cloud Run Microservice

Simple workflow:
1. User sends prompt
2. Classify domain (photography/diagrams/art/products)
3. Enhance with professional template
4. Call Gemini API
5. Return image

No Kubernetes, no PostgreSQL, no Redis Queue - just works!
"""

from flask import Flask, request, jsonify, Response
import asyncio
import os
import base64
from datetime import datetime, UTC
from typing import Any, Dict, List, Optional

# Our simple components
from domain_classifier import DomainClassifier
from template_engine import TemplateEngine
from gemini_client import GeminiClient
from brand_profile_manager import BrandProfileManager

# Initialize Flask app
app = Flask(__name__)

# Initialize components
classifier = DomainClassifier()
template_engine = TemplateEngine()
brand_profile_manager = BrandProfileManager()

VALID_QUALITIES = {"basic", "detailed", "expert"}
VALID_MODELS = {"flash", "pro"}
VALID_FORMATS = {"base64"}
MAX_BATCH_SIZE = 20
DEFAULT_BATCH_CONCURRENCY = 3
MAX_BATCH_CONCURRENCY = 10


# Helper to run async code in Flask
def run_async(coro):
    """Run async function in Flask (Flask doesn't support async natively)"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


def _validate_and_parse_request(data: Dict[str, Any]) -> Dict[str, Any]:
    if not data or "prompt" not in data:
        raise ValueError("Missing 'prompt' in request")

    user_prompt = data["prompt"]
    if not isinstance(user_prompt, str) or not user_prompt.strip():
        raise ValueError("'prompt' must be a non-empty string")

    quality = data.get("quality", "detailed")
    model = data.get("model", "flash")
    output_format = data.get("format", "base64")
    aspect_ratio = data.get("aspect_ratio")
    image_size = data.get("image_size")
    brand_profile = data.get("brand_profile")

    if quality not in VALID_QUALITIES:
        raise ValueError(
            f"Invalid quality: {quality}. Must be basic/detailed/expert"
        )
    if model not in VALID_MODELS:
        raise ValueError(
            f"Invalid model: {model}. Must be flash/pro"
        )
    if output_format not in VALID_FORMATS:
        raise ValueError(
            f"Unsupported format: {output_format}"
        )
    if brand_profile and not isinstance(brand_profile, str):
        raise ValueError("'brand_profile' must be a string")

    return {
        "user_prompt": user_prompt.strip(),
        "quality": quality,
        "model": model,
        "format": output_format,
        "aspect_ratio": aspect_ratio,
        "image_size": image_size,
        "brand_profile": brand_profile
    }


def _build_enhanced_prompt(parsed: Dict[str, Any]) -> Dict[str, Any]:
    user_prompt = parsed["user_prompt"]
    quality = parsed["quality"]
    brand_profile = parsed["brand_profile"]

    # Step 1: Classify domain
    domain, confidence = classifier.classify_with_confidence(user_prompt)

    # Step 2: Suggest subcategory
    subcategory = template_engine.suggest_subcategory(user_prompt, domain)

    # Step 3: Enhance prompt
    enhanced_prompt = template_engine.enhance(
        user_prompt,
        domain=domain,
        quality=quality,
        subcategory=subcategory
    )

    # Step 4: Apply optional brand profile
    enhanced_prompt = brand_profile_manager.apply(enhanced_prompt, brand_profile)

    return {
        "enhanced_prompt": enhanced_prompt,
        "domain": domain,
        "subcategory": subcategory,
        "domain_confidence": confidence
    }


def _format_image_response(
    parsed: Dict[str, Any],
    prompt_info: Dict[str, Any],
    result: Dict[str, Any]
) -> Dict[str, Any]:
    image_b64 = base64.b64encode(result["image_data"]).decode("utf-8")
    image_data_uri = f"data:{result['mime_type']};base64,{image_b64}"

    return {
        "image": image_data_uri,
        "enhanced_prompt": prompt_info["enhanced_prompt"],
        "domain": prompt_info["domain"],
        "subcategory": prompt_info["subcategory"],
        "model": parsed["model"],
        "metadata": {
            "original_prompt": parsed["user_prompt"],
            "quality": parsed["quality"],
            "domain_confidence": prompt_info["domain_confidence"],
            "image_size_bytes": len(result["image_data"]),
            "mime_type": result["mime_type"],
            "aspect_ratio": parsed["aspect_ratio"],
            "image_size": parsed["image_size"],
            "brand_profile": parsed["brand_profile"],
            "timestamp": datetime.now(UTC).isoformat()
        }
    }


async def _generate_single_async(parsed: Dict[str, Any]) -> Dict[str, Any]:
    prompt_info = _build_enhanced_prompt(parsed)

    async with GeminiClient() as client:
        result = await client.generate_image(
            prompt_info["enhanced_prompt"],
            model=parsed["model"],
            aspect_ratio=parsed["aspect_ratio"],
            image_size=parsed["image_size"]
        )

    return _format_image_response(parsed, prompt_info, result)


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint for Cloud Run"""
    return jsonify({
        "status": "healthy",
        "service": "nanobanana-image-generation",
        "timestamp": datetime.now(UTC).isoformat()
    })


@app.route("/generate", methods=["POST"])
def generate_image():
    """
    Generate image from text prompt.

    Request:
        {
            "prompt": "headshot of a CEO",
            "quality": "detailed",  # optional: basic/detailed/expert
            "model": "flash",       # optional: flash/pro
            "aspect_ratio": "16:9", # optional: 1:1/16:9/9:16/4:3/3:4
            "image_size": "2K",     # optional: 1K/2K/4K
            "brand_profile": "modern_tech", # optional: named brand profile
            "format": "base64"      # optional: base64/url
        }

    Response:
        {
            "image": "data:image/png;base64,...",
            "enhanced_prompt": "professional corporate headshot...",
            "domain": "photography",
            "subcategory": "portrait",
            "model": "flash",
            "metadata": {...}
        }

    Example:
        curl -X POST http://localhost:8080/generate \\
             -H "Content-Type: application/json" \\
             -d '{"prompt": "sunset over mountains"}'
    """
    try:
        data = request.get_json()
        parsed = _validate_and_parse_request(data)
        response = run_async(_generate_single_async(parsed))
        return jsonify(response), 200

    except ValueError as e:
        error_message = str(e)
        allowed_prefixes = (
            "Missing",
            "Invalid",
            "Unsupported",
            "Unknown",
            "'prompt'",
            "'brand_profile'"
        )
        if error_message.startswith(allowed_prefixes):
            return jsonify({"error": error_message}), 400
        return jsonify({"error": "Invalid request parameters"}), 400

    except Exception as e:
        # Log error (in production, use proper logging)
        print(f"ERROR: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/generate/batch", methods=["POST"])
def generate_batch():
    """
    Batch image generation endpoint.

    Request:
        {
          "requests": [
            {"prompt": "architecture diagram", "model": "pro"},
            {"prompt": "product hero shot", "aspect_ratio": "1:1"}
          ],
          "max_concurrent": 3
        }
    """
    try:
        data = request.get_json() or {}
        requests_data = data.get("requests")

        if not isinstance(requests_data, list) or not requests_data:
            return jsonify({"error": "Missing non-empty 'requests' array"}), 400

        if len(requests_data) > MAX_BATCH_SIZE:
            return jsonify({
                "error": f"Batch size exceeds limit ({MAX_BATCH_SIZE})"
            }), 400

        max_concurrent = data.get("max_concurrent", DEFAULT_BATCH_CONCURRENCY)
        if not isinstance(max_concurrent, int) or not (1 <= max_concurrent <= MAX_BATCH_CONCURRENCY):
            return jsonify({
                "error": (
                    f"Invalid max_concurrent: {max_concurrent}. "
                    f"Must be integer between 1 and {MAX_BATCH_CONCURRENCY}"
                )
            }), 400

        async def process_batch(items: List[Dict[str, Any]]) -> Dict[str, Any]:
            semaphore = asyncio.Semaphore(max_concurrent)

            async with GeminiClient() as client:
                async def process_item(index: int, item: Dict[str, Any]) -> Dict[str, Any]:
                    try:
                        parsed = _validate_and_parse_request(item)
                        prompt_info = _build_enhanced_prompt(parsed)

                        async with semaphore:
                            result = await client.generate_image(
                                prompt_info["enhanced_prompt"],
                                model=parsed["model"],
                                aspect_ratio=parsed["aspect_ratio"],
                                image_size=parsed["image_size"]
                            )

                        payload = _format_image_response(parsed, prompt_info, result)
                        payload["status"] = "success"
                        payload["index"] = index
                        return payload

                    except Exception as err:
                        return {
                            "status": "error",
                            "index": index,
                            "error": str(err),
                            "prompt": item.get("prompt")
                        }

                tasks = [process_item(i, item) for i, item in enumerate(items)]
                results = await asyncio.gather(*tasks)
                return {"results": results}

        result = run_async(process_batch(requests_data))
        success_count = sum(1 for r in result["results"] if r["status"] == "success")
        return jsonify({
            "total": len(result["results"]),
            "succeeded": success_count,
            "failed": len(result["results"]) - success_count,
            "results": result["results"]
        }), 200

    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/classify", methods=["POST"])
def classify():
    """
    Classify prompt domain without generating image (useful for debugging).

    Request:
        {"prompt": "headshot of a CEO"}

    Response:
        {
            "domain": "photography",
            "confidence": 0.85,
            "scores": {"photography": 3, "diagrams": 0, ...},
            "suggested_subcategory": "portrait"
        }
    """
    try:
        data = request.get_json()
        if not data or "prompt" not in data:
            return jsonify({"error": "Missing 'prompt' in request"}), 400

        user_prompt = data["prompt"]

        # Classify
        domain, confidence = classifier.classify_with_confidence(user_prompt)
        scores = classifier.get_all_scores(user_prompt)
        subcategory = template_engine.suggest_subcategory(user_prompt, domain)

        return jsonify({
            "domain": domain,
            "confidence": confidence,
            "scores": scores,
            "suggested_subcategory": subcategory,
            "available_subcategories": template_engine.get_available_subcategories(domain)
        }), 200

    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/enhance", methods=["POST"])
def enhance():
    """
    Enhance prompt without generating image (useful for testing templates).

    Request:
        {
            "prompt": "headshot of a CEO",
            "domain": "photography",      # optional (auto-detected if omitted)
            "subcategory": "portrait",     # optional (auto-suggested if omitted)
            "quality": "expert",           # optional (default: detailed)
            "brand_profile": "modern_tech" # optional
        }

    Response:
        {
            "enhanced_prompt": "professional corporate headshot of CEO...",
            "domain": "photography",
            "subcategory": "portrait",
            "quality": "expert"
        }
    """
    try:
        data = request.get_json()
        if not data or "prompt" not in data:
            return jsonify({"error": "Missing 'prompt' in request"}), 400

        user_prompt = data["prompt"]
        domain = data.get("domain")
        subcategory = data.get("subcategory")
        quality = data.get("quality", "detailed")
        brand_profile = data.get("brand_profile")

        # Auto-detect domain if not provided
        if not domain:
            domain, _ = classifier.classify_with_confidence(user_prompt)

        # Auto-suggest subcategory if not provided
        if not subcategory:
            subcategory = template_engine.suggest_subcategory(user_prompt, domain)

        # Enhance
        enhanced = template_engine.enhance(
            user_prompt,
            domain=domain,
            quality=quality,
            subcategory=subcategory
        )
        enhanced = brand_profile_manager.apply(enhanced, brand_profile)

        return jsonify({
            "enhanced_prompt": enhanced,
            "domain": domain,
            "subcategory": subcategory,
            "quality": quality,
            "brand_profile": brand_profile,
            "original_prompt": user_prompt
        }), 200

    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/brand-profiles", methods=["GET"])
def brand_profiles():
    """List available brand profiles and full definitions."""
    return jsonify({
        "profiles": brand_profile_manager.profiles,
        "available_profiles": brand_profile_manager.list_profiles()
    }), 200


@app.route("/", methods=["GET"])
def index():
    """
    Landing page with API documentation.
    """
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>NanoBanana Image Generation API</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                line-height: 1.6;
            }
            h1 { color: #FF9900; }
            h2 { color: #0066CC; }
            code {
                background: #f4f4f4;
                padding: 2px 5px;
                border-radius: 3px;
            }
            pre {
                background: #f4f4f4;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
            }
            .endpoint {
                background: #e8f4f8;
                padding: 10px;
                border-left: 4px solid #0066CC;
                margin: 10px 0;
            }
        </style>
    </head>
    <body>
        <h1>🍌 NanoBanana Image Generation API</h1>
        <p>Simple, fast, jargon-free image generation using Google's Gemini API.</p>

        <h2>Endpoints</h2>

        <div class="endpoint">
            <h3>POST /generate</h3>
            <p>Generate image from text prompt</p>
            <pre>{
  "prompt": "headshot of a CEO",
  "quality": "detailed",  // optional: basic/detailed/expert
  "model": "flash",       // optional: flash/pro
  "aspect_ratio": "16:9", // optional: 1:1/16:9/9:16/4:3/3:4
  "image_size": "2K",     // optional: 1K/2K/4K
  "brand_profile": "modern_tech" // optional
}</pre>
        </div>

        <div class="endpoint">
            <h3>POST /generate/batch</h3>
            <p>Generate multiple images with bounded concurrency</p>
            <pre>{
  "requests": [
    {"prompt": "architecture diagram", "model": "pro"},
    {"prompt": "product shot", "aspect_ratio": "1:1"}
  ],
  "max_concurrent": 3
}</pre>
        </div>

        <div class="endpoint">
            <h3>POST /classify</h3>
            <p>Classify prompt domain (photography/diagrams/art/products)</p>
            <pre>{"prompt": "AWS architecture diagram"}</pre>
        </div>

        <div class="endpoint">
            <h3>POST /enhance</h3>
            <p>Enhance prompt with professional specifications</p>
            <pre>{"prompt": "sunset over mountains", "quality": "expert"}</pre>
        </div>

        <div class="endpoint">
            <h3>GET /health</h3>
            <p>Health check endpoint</p>
        </div>

        <div class="endpoint">
            <h3>GET /brand-profiles</h3>
            <p>List available brand profiles and constraints</p>
        </div>

        <h2>Quick Start</h2>
        <pre>curl -X POST http://localhost:8080/generate \\
  -H "Content-Type: application/json" \\
  -d '{"prompt": "professional headshot of a CEO"}'</pre>

        <p><strong>No Kubernetes, no PostgreSQL, no Redis Queue - just works!</strong></p>
    </body>
    </html>
    """
    return Response(html, mimetype="text/html")


if __name__ == "__main__":
    # Local development server
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
