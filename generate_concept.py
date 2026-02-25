#!/usr/bin/env python3
"""
Generate Context Engineering Concept Images

Replaces 20 individual generate_c*.py scripts with a single configurable script.
Usage:
    python generate_concept.py C01          # Generate one concept
    python generate_concept.py C01 C05 C10  # Generate specific concepts
    python generate_concept.py --all        # Generate all concepts
    python generate_concept.py --list       # List available concepts
"""

import asyncio
import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.gemini_client import GeminiClient

# Base path for docs images, configurable via environment variable.
# Set NANOBANANA_DOCS_PATH to your local docs/images/context-engineering directory.
DOCS_BASE = Path(os.environ.get(
    "NANOBANANA_DOCS_PATH",
    Path(__file__).parent / "docs" / "images" / "context-engineering",
))

# Data-driven configuration: all 20 concepts in one place.
# Paths are relative to DOCS_BASE (set via NANOBANANA_DOCS_PATH env var).
CONCEPTS = {
    "C01": {
        "title": "Context Window Fundamentals",
        "prompt_path": DOCS_BASE / "batch-1" / "C01-prompt.txt",
        "output_path": DOCS_BASE / "batch-1" / "C01-context-window.png",
    },
    "C02": {
        "title": "7-Layer Context Stack",
        "prompt_path": DOCS_BASE / "batch-2" / "C02-prompt.txt",
        "output_path": DOCS_BASE / "batch-2" / "C02-7-layer-stack.png",
    },
    "C03": {
        "title": "Token Budget Management",
        "prompt_path": DOCS_BASE / "batch-1" / "C03-prompt.txt",
        "output_path": DOCS_BASE / "batch-1" / "C03-token-budget.png",
    },
    "C04": {
        "title": "Context Overflow Problem",
        "prompt_path": DOCS_BASE / "batch-1" / "C04-prompt.txt",
        "output_path": DOCS_BASE / "batch-1" / "C04-context-overflow.png",
    },
    "C05": {
        "title": "RAG Pipeline Architecture",
        "prompt_path": DOCS_BASE / "batch-1" / "C05-prompt.txt",
        "output_path": DOCS_BASE / "batch-1" / "C05-rag-pipeline.png",
    },
    "C06": {
        "title": "Multi-Stage RAG Retrieval",
        "prompt_path": DOCS_BASE / "batch-2" / "C06-prompt.txt",
        "output_path": DOCS_BASE / "batch-2" / "C06-multistage-rag.png",
    },
    "C07": {
        "title": "Intelligent Chunking Strategies",
        "prompt_path": DOCS_BASE / "batch-2" / "C07-prompt.txt",
        "output_path": DOCS_BASE / "batch-2" / "C07-chunking-strategies.png",
    },
    "C08": {
        "title": "Hybrid Search Architecture",
        "prompt_path": DOCS_BASE / "batch-2" / "C08-prompt.txt",
        "output_path": DOCS_BASE / "batch-2" / "C08-hybrid-search.png",
    },
    "C09": {
        "title": "Prompt Compression Techniques",
        "prompt_path": DOCS_BASE / "batch-3" / "C09-prompt.txt",
        "output_path": DOCS_BASE / "batch-3" / "C09-prompt-compression.png",
    },
    "C10": {
        "title": "Memory Compression Techniques",
        "prompt_path": DOCS_BASE / "batch-2" / "C10-prompt.txt",
        "output_path": DOCS_BASE / "batch-2" / "C10-memory-compression.png",
    },
    "C11": {
        "title": "Attention Mechanisms",
        "prompt_path": DOCS_BASE / "batch-3" / "C11-prompt.txt",
        "output_path": DOCS_BASE / "batch-3" / "C11-attention-mechanisms.png",
    },
    "C12": {
        "title": "Dynamic Context Routing",
        "prompt_path": DOCS_BASE / "batch-3" / "C12-prompt.txt",
        "output_path": DOCS_BASE / "batch-3" / "C12-dynamic-routing.png",
    },
    "C13": {
        "title": "Context Pruning Strategies",
        "prompt_path": DOCS_BASE / "batch-4" / "C13-prompt.txt",
        "output_path": DOCS_BASE / "batch-4" / "C13-context-pruning.png",
    },
    "C14": {
        "title": "Semantic Caching",
        "prompt_path": DOCS_BASE / "batch-3" / "C14-prompt.txt",
        "output_path": DOCS_BASE / "batch-3" / "C14-semantic-caching.png",
    },
    "C15": {
        "title": "Multi-Turn Context Management",
        "prompt_path": DOCS_BASE / "batch-4" / "C15-prompt.txt",
        "output_path": DOCS_BASE / "batch-4" / "C15-multiturn-management.png",
    },
    "C16": {
        "title": "Context-Aware Prompt Templates",
        "prompt_path": DOCS_BASE / "batch-4" / "C16-prompt.txt",
        "output_path": DOCS_BASE / "batch-4" / "C16-prompt-templates.png",
    },
    "C17": {
        "title": "Context-Aware Error Recovery",
        "prompt_path": DOCS_BASE / "batch-3" / "C17-prompt.txt",
        "output_path": DOCS_BASE / "batch-3" / "C17-error-recovery.png",
    },
    "C18": {
        "title": "Adaptive Context Windowing",
        "prompt_path": DOCS_BASE / "batch-4" / "C18-prompt.txt",
        "output_path": DOCS_BASE / "batch-4" / "C18-adaptive-windowing.png",
    },
    "C19": {
        "title": "Cross-Session Context Persistence",
        "prompt_path": DOCS_BASE / "batch-4" / "C19-prompt.txt",
        "output_path": DOCS_BASE / "batch-4" / "C19-cross-session-persistence.png",
    },
    "C20": {
        "title": "Future - Infinite Context",
        "prompt_path": DOCS_BASE / "batch-4" / "C20-prompt.txt",
        "output_path": DOCS_BASE / "batch-4" / "C20-future-infinite-context.png",
    },
}


async def generate_concept(concept_id: str) -> bool:
    """Generate a single concept image. Returns True on success."""
    config = CONCEPTS[concept_id]
    prompt_path = Path(config["prompt_path"])
    output_path = Path(config["output_path"])

    print(f"🎨 Generating {concept_id}: {config['title']}")
    print(f"   Model: Gemini 3 Pro Image (gemini-3-pro-image-preview)")

    prompt = prompt_path.read_text()

    async with GeminiClient() as client:
        try:
            result = await client.generate_image(prompt, model="pro")

            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(result["image_data"])

            size_mb = len(result["image_data"]) / (1024 * 1024)
            print(f"   ✅ Success! Image saved ({size_mb:.2f} MB)")
            print(f"   📁 {output_path}")
            return True

        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False


async def generate_many(concept_ids: list[str]):
    """Generate multiple concept images sequentially."""
    succeeded, failed = 0, 0
    for concept_id in concept_ids:
        print()
        if await generate_concept(concept_id):
            succeeded += 1
        else:
            failed += 1

    print()
    print(f"Done: {succeeded} succeeded, {failed} failed out of {len(concept_ids)} total")


def list_concepts():
    """Print available concepts."""
    print("Available concepts:")
    for concept_id, config in CONCEPTS.items():
        print(f"  {concept_id}: {config['title']}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate context engineering concept images"
    )
    parser.add_argument(
        "concepts",
        nargs="*",
        help="Concept IDs to generate (e.g., C01 C05 C10)",
    )
    parser.add_argument("--all", action="store_true", help="Generate all concepts")
    parser.add_argument("--list", action="store_true", help="List available concepts")

    args = parser.parse_args()

    if args.list:
        list_concepts()
        return

    if args.all:
        concept_ids = list(CONCEPTS.keys())
    elif args.concepts:
        concept_ids = [c.upper() for c in args.concepts]
        for cid in concept_ids:
            if cid not in CONCEPTS:
                print(f"Unknown concept: {cid}")
                print(f"Valid concepts: {', '.join(CONCEPTS.keys())}")
                sys.exit(1)
    else:
        parser.print_help()
        return

    asyncio.run(generate_many(concept_ids))


if __name__ == "__main__":
    main()
