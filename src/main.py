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
from datetime import datetime
from typing import Dict, Optional

# Our simple components
from domain_classifier import DomainClassifier
from template_engine import TemplateEngine
from gemini_client import GeminiClient

# Initialize Flask app
app = Flask(__name__)

# Initialize components
classifier = DomainClassifier()
template_engine = TemplateEngine()


# Helper to run async code in Flask
def run_async(coro):
    """Run async function in Flask (Flask doesn't support async natively)"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint for Cloud Run"""
    return jsonify({
        "status": "healthy",
        "service": "nanobanana-image-generation",
        "timestamp": datetime.utcnow().isoformat()
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
        # Parse request
        data = request.get_json()
        if not data or "prompt" not in data:
            return jsonify({"error": "Missing 'prompt' in request"}), 400

        user_prompt = data["prompt"]
        quality = data.get("quality", "detailed")
        model = data.get("model", "flash")
        output_format = data.get("format", "base64")

        # Validate quality
        if quality not in ["basic", "detailed", "expert"]:
            return jsonify({
                "error": f"Invalid quality: {quality}. Must be basic/detailed/expert"
            }), 400

        # Validate model
        if model not in ["flash", "pro"]:
            return jsonify({
                "error": f"Invalid model: {model}. Must be flash/pro"
            }), 400

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

        # Step 4: Generate image
        async def generate():
            async with GeminiClient() as client:
                result = await client.generate_image(enhanced_prompt, model=model)
                return result

        result = run_async(generate())

        # Step 5: Format response
        if output_format == "base64":
            # Return base64-encoded image
            image_b64 = base64.b64encode(result["image_data"]).decode("utf-8")
            image_data_uri = f"data:{result['mime_type']};base64,{image_b64}"

            response = {
                "image": image_data_uri,
                "enhanced_prompt": enhanced_prompt,
                "domain": domain,
                "subcategory": subcategory,
                "model": model,
                "metadata": {
                    "original_prompt": user_prompt,
                    "quality": quality,
                    "domain_confidence": confidence,
                    "image_size_bytes": len(result["image_data"]),
                    "mime_type": result["mime_type"],
                    "timestamp": datetime.utcnow().isoformat()
                }
            }

            return jsonify(response), 200

        else:
            return jsonify({"error": f"Unsupported format: {output_format}"}), 400

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        # Log error (in production, use proper logging)
        print(f"ERROR: {e}")
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500


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
        return jsonify({"error": str(e)}), 500


@app.route("/enhance", methods=["POST"])
def enhance():
    """
    Enhance prompt without generating image (useful for testing templates).

    Request:
        {
            "prompt": "headshot of a CEO",
            "domain": "photography",      # optional (auto-detected if omitted)
            "subcategory": "portrait",     # optional (auto-suggested if omitted)
            "quality": "expert"            # optional (default: detailed)
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

        return jsonify({
            "enhanced_prompt": enhanced,
            "domain": domain,
            "subcategory": subcategory,
            "quality": quality,
            "original_prompt": user_prompt
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
  "model": "flash"        // optional: flash/pro
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
