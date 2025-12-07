# Async Batch Image Generation Pattern - The Essential Extraction

**Extracted from NanoBanana codebase using comonadic pattern analysis**

## Core Insight: What Is The Essence?

After analyzing `gemini_client.py`, `test_concurrent.py`, and `generate_examples.py`, the pattern reduces to:

**The core computation**: `prompt → API call → image bytes`

**The simplest way to do N of these**: `asyncio.gather()` or `asyncio.as_completed()`

**Stream results as they complete**: `async for` over `as_completed()`

---

## Pattern 1: Simple Concurrent Batch (No Streaming)

**Use when**: You want all results at once after all complete.

```python
import asyncio
from typing import List, Dict
from gemini_client import GeminiClient

async def generate_batch(prompts: List[str], max_concurrent: int = 5) -> List[Dict]:
    """
    Generate images concurrently with controlled parallelism.

    Args:
        prompts: List of text prompts
        max_concurrent: Max concurrent API calls

    Returns:
        List of results (same order as prompts)
    """
    semaphore = asyncio.Semaphore(max_concurrent)

    async def generate_one(prompt: str, index: int) -> Dict:
        async with semaphore:
            async with GeminiClient() as client:
                result = await client.generate_image(prompt, model="flash")
                return {
                    "index": index,
                    "prompt": prompt,
                    "image_data": result["image_data"],
                    "size_mb": len(result["image_data"]) / (1024 * 1024)
                }

    # Launch all tasks concurrently, respect semaphore limit
    tasks = [generate_one(p, i) for i, p in enumerate(prompts)]
    return await asyncio.gather(*tasks)


# Usage
async def main():
    prompts = [
        "Professional headshot of a CEO",
        "Mountain landscape at sunset",
        "Coffee cup on wooden table"
    ]

    results = await generate_batch(prompts, max_concurrent=2)

    # All results available at once
    for r in results:
        print(f"[{r['index']}] {r['size_mb']:.2f} MB - {r['prompt']}")


asyncio.run(main())
```

**Complexity**: Minimal. Uses Python's built-in `gather()` with semaphore for concurrency control.

---

## Pattern 2: Streaming Results (As They Complete)

**Use when**: You want to process/save images immediately as they finish (don't wait for all).

```python
import asyncio
from typing import List, Dict, AsyncGenerator
from gemini_client import GeminiClient

async def generate_batch_streaming(
    prompts: List[str],
    max_concurrent: int = 5
) -> AsyncGenerator[Dict, None]:
    """
    Generate images concurrently, yield results as they complete.

    Args:
        prompts: List of text prompts
        max_concurrent: Max concurrent API calls

    Yields:
        Results in completion order (not input order)
    """
    semaphore = asyncio.Semaphore(max_concurrent)

    async def generate_one(prompt: str, index: int) -> Dict:
        async with semaphore:
            async with GeminiClient() as client:
                result = await client.generate_image(prompt, model="flash")
                return {
                    "index": index,
                    "prompt": prompt,
                    "image_data": result["image_data"],
                    "size_mb": len(result["image_data"]) / (1024 * 1024)
                }

    # Create all tasks
    tasks = [generate_one(p, i) for i, p in enumerate(prompts)]

    # Yield results as they complete
    for coro in asyncio.as_completed(tasks):
        yield await coro


# Usage
async def main():
    prompts = [
        "Professional headshot of a CEO",
        "Mountain landscape at sunset",
        "Coffee cup on wooden table"
    ]

    # Process results as they stream in
    async for result in generate_batch_streaming(prompts, max_concurrent=2):
        print(f"✓ [{result['index']}] {result['size_mb']:.2f} MB - {result['prompt']}")

        # Save immediately (don't wait for all)
        filename = f"image_{result['index']:02d}.png"
        with open(filename, "wb") as f:
            f.write(result["image_data"])
        print(f"  Saved: {filename}")


asyncio.run(main())
```

**Complexity**: Minimal. Uses `asyncio.as_completed()` to yield results as they finish.

---

## Pattern 3: With Progress Tracking

**Use when**: You want real-time progress updates during batch generation.

```python
import asyncio
from typing import List, Dict, AsyncGenerator
from gemini_client import GeminiClient

async def generate_batch_with_progress(
    prompts: List[str],
    max_concurrent: int = 5
) -> AsyncGenerator[Dict, None]:
    """
    Generate images concurrently with progress tracking.

    Yields:
        Progress updates and results
    """
    semaphore = asyncio.Semaphore(max_concurrent)
    total = len(prompts)
    completed = 0

    async def generate_one(prompt: str, index: int) -> Dict:
        async with semaphore:
            async with GeminiClient() as client:
                result = await client.generate_image(prompt, model="flash")
                return {
                    "index": index,
                    "prompt": prompt,
                    "image_data": result["image_data"],
                    "size_mb": len(result["image_data"]) / (1024 * 1024)
                }

    tasks = [generate_one(p, i) for i, p in enumerate(prompts)]

    for coro in asyncio.as_completed(tasks):
        result = await coro
        completed += 1

        # Yield progress
        yield {
            "type": "progress",
            "completed": completed,
            "total": total,
            "percent": (completed / total) * 100
        }

        # Yield result
        yield {
            "type": "result",
            **result
        }


# Usage
async def main():
    prompts = [
        "Professional headshot of a CEO",
        "Mountain landscape at sunset",
        "Coffee cup on wooden table",
        "Modern office workspace",
        "Tech startup team meeting"
    ]

    async for item in generate_batch_with_progress(prompts, max_concurrent=2):
        if item["type"] == "progress":
            print(f"Progress: {item['completed']}/{item['total']} ({item['percent']:.0f}%)")

        elif item["type"] == "result":
            print(f"  ✓ [{item['index']}] {item['size_mb']:.2f} MB - {item['prompt']}")


asyncio.run(main())
```

**Complexity**: Still minimal. Just adds progress tracking to Pattern 2.

---

## Key Design Decisions

### 1. Why `asyncio.Semaphore`?

**Purpose**: Limit concurrent API calls to avoid rate limits.

**Alternative considered**: Manual delay between requests (15s stagger in `test_concurrent.py`)
- **Rejected**: Unnecessarily slow. If API can handle 5 concurrent, use 5 concurrent.
- **When to use delays**: Only if API documentation explicitly requires it.

**Reality check**: Gemini API handles concurrency fine. Semaphore is enough.

### 2. Why `asyncio.gather()` vs `asyncio.as_completed()`?

| Pattern | Use Case | Order | Blocking |
|---------|----------|-------|----------|
| `gather()` | Get all results at once | Input order preserved | Wait for all |
| `as_completed()` | Stream results as they finish | Completion order | Yield immediately |

**Choose `gather()`**: When you need results in input order or want to wait for all.

**Choose `as_completed()`**: When you want to process/save immediately as each completes.

### 3. Why NO exponential backoff in the batch wrapper?

**Answer**: It's already in `GeminiClient.generate_image()` (lines 106-157).

**Principle**: Don't duplicate retry logic. The client handles it.

**When to add**: Only if you need *batch-level* retry (e.g., "retry entire batch if 50% fail").

### 4. Why NO artificial delays?

**From `test_concurrent.py`**:
```python
delay = index * self.delay_seconds  # 15 second stagger
await asyncio.sleep(delay)
```

**Analysis**: This was added due to rate limiting research, but it's *overly conservative*.

**Reality**:
- Gemini API supports concurrency
- Semaphore already controls max concurrent
- Delays just make things slower

**When to use delays**: Only if you observe 429 errors even with semaphore.

---

## What We Removed (And Why)

### ❌ Removed: Complex retry logic in batch wrapper
**Why**: Already in `GeminiClient.generate_image()` (max_retries=3, exponential backoff)

### ❌ Removed: Staggered delays (15s between starts)
**Why**: Unnecessary if API supports concurrency. Semaphore is enough.

### ❌ Removed: Complex error tracking/categorization
**Why**: Just let exceptions propagate or use simple try/except in wrapper.

### ❌ Removed: Domain classification/template enhancement
**Why**: Not part of the *async batch pattern*. That's business logic.

---

## The Comonadic View

**Extract operation**: What is the *local* computation?
- `async def generate_one(prompt) → result`

**Extend operation**: How do we *contextualize* it?
- Wrap in semaphore for concurrency control
- Wrap in `as_completed()` for streaming
- Add index for tracking

**Simplicity**: The pattern is just Python's built-in async primitives. No magic.

---

## Complete Reference Implementation

```python
"""
Async Batch Image Generation - The Essential Pattern

Extracted from NanoBanana via comonadic analysis.
This is the SIMPLEST version that works.
"""

import asyncio
from typing import List, Dict, AsyncGenerator, Optional
from pathlib import Path


async def generate_batch(
    prompts: List[str],
    client_factory,  # e.g., lambda: GeminiClient()
    max_concurrent: int = 5,
    save_dir: Optional[Path] = None
) -> AsyncGenerator[Dict, None]:
    """
    Generate images concurrently, yield results as they complete.

    Args:
        prompts: List of text prompts
        client_factory: Function that creates client instance
        max_concurrent: Max concurrent API calls
        save_dir: Optional directory to save images

    Yields:
        Result dicts with index, prompt, image_data, size_mb
    """
    semaphore = asyncio.Semaphore(max_concurrent)

    async def generate_one(prompt: str, index: int) -> Dict:
        async with semaphore:
            async with client_factory() as client:
                result = await client.generate_image(prompt, model="flash")

                image_data = result["image_data"]

                # Optionally save
                if save_dir:
                    filepath = save_dir / f"image_{index:03d}.png"
                    with open(filepath, "wb") as f:
                        f.write(image_data)
                else:
                    filepath = None

                return {
                    "index": index,
                    "prompt": prompt,
                    "image_data": image_data,
                    "size_mb": len(image_data) / (1024 * 1024),
                    "filepath": filepath
                }

    tasks = [generate_one(p, i) for i, p in enumerate(prompts)]

    for coro in asyncio.as_completed(tasks):
        yield await coro


# Usage Example
async def main():
    from gemini_client import GeminiClient

    prompts = [
        "Professional headshot of a CEO",
        "Mountain landscape at sunset",
        "Coffee cup on wooden table"
    ]

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    print(f"Generating {len(prompts)} images...")

    completed = 0
    async for result in generate_batch(
        prompts,
        client_factory=GeminiClient,
        max_concurrent=3,
        save_dir=output_dir
    ):
        completed += 1
        print(
            f"[{completed}/{len(prompts)}] "
            f"{result['size_mb']:.2f} MB - {result['prompt'][:50]}"
        )
        if result['filepath']:
            print(f"  → {result['filepath']}")

    print("✅ Done!")


if __name__ == "__main__":
    asyncio.run(main())
```

**Lines of code**: ~60 (including comments)

**External dependencies**: Just `asyncio` (stdlib)

**Complexity**: Minimal - uses Python's built-in async primitives

---

## When To Use Each Pattern

| Use Case | Pattern | Why |
|----------|---------|-----|
| Generate 10 images, save all at end | Pattern 1 (`gather`) | Simple, order preserved |
| Generate 100 images, save as they finish | Pattern 2 (`as_completed`) | Don't wait, stream results |
| Show progress bar while generating | Pattern 3 (with progress) | Real-time feedback |
| Production API with monitoring | Reference Implementation | Clean, extensible |

---

## Performance Characteristics

**Time complexity**: O(n/k) where n = prompts, k = max_concurrent

**Memory**: O(k) active tasks + O(n) results (if collecting all)

**Network**: Controlled by semaphore (no rate limit issues)

**Example**: 100 images, 5 concurrent, 3s per image:
- Sequential: 100 × 3s = 300s (5 minutes)
- Concurrent: 100 ÷ 5 × 3s = 60s (1 minute)

---

## Summary: What We Learned

1. **Core operation**: `prompt → API call → image bytes` (async function)

2. **Concurrency control**: `asyncio.Semaphore(max_concurrent)`

3. **Batch execution**:
   - `asyncio.gather()` for all-at-once
   - `asyncio.as_completed()` for streaming

4. **What to avoid**:
   - Artificial delays (if API supports concurrency)
   - Duplicate retry logic (put it in client)
   - Over-engineering (KISS principle)

5. **The comonadic insight**:
   - Extract = local computation (generate one image)
   - Extend = contextual wrapper (semaphore, streaming, progress)
   - Keep them separate and composable

**Total complexity**: ~60 lines of readable Python

**Dependencies**: Just stdlib `asyncio`

**Elegance**: You'd be proud to show this to another developer

---

## Further Reading

- `gemini_client.py` - Client with retry logic (lines 52-158)
- `test_concurrent.py` - Over-engineered version with delays
- `generate_examples.py` - Sequential version (simple loop)

**Recommendation**: Start with Pattern 2 (streaming). It's the sweet spot of simplicity and utility.
