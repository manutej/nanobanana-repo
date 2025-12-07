# Gemini Batch API Research - Image Generation at Scale

**Date**: 2025-12-07
**API Version**: Gemini v1beta
**Model**: `gemini-2.5-flash-image`

---

## Executive Summary

**Current Problem**: Sequential image generation hits rate limits after 1-2 requests, causing 80-90% failure rate.

**Root Cause**: Using individual synchronous requests instead of Gemini's native batch API or proper async concurrency.

**Solution**: Two approaches based on volume:
- **High Volume (10+ images)**: Use Batch API (`/v1beta/batches`)
- **Low Volume (<10 images)**: Use async concurrency with rate limiting

---

## Gemini Batch API Architecture

### Overview

Gemini provides a **native batch processing API** specifically designed for high-volume image generation:

```
Endpoint: POST /v1beta/batches
Model: gemini-2.5-flash-image
Input: JSONL file (uploaded via File API)
Turnaround: Up to 24 hours
Rate Limits: Significantly higher than individual requests
```

### Workflow

```
1. Create JSONL file with batch requests
2. Upload JSONL file → files/your-file-id
3. Create batch job → batches/job-id
4. Poll job status (10 second intervals)
5. Download results JSONL file
6. Parse and extract images
```

### Key Benefits

| Feature | Individual Requests | Batch API |
|---------|-------------------|-----------|
| **Rate Limit** | 1-2 requests/minute (free tier) | 1000s of requests/batch |
| **Turnaround** | Instant (3 seconds) | Up to 24 hours |
| **Cost** | Same per request | Same per request |
| **Complexity** | Simple | Moderate |
| **Best For** | <10 images, real-time | 10+ images, background |

---

## Implementation: Batch API (Python)

### Complete Workflow

```python
import json
import time
from google import genai
from google.genai import types

client = genai.Client()

# Step 1: Create JSONL file with batch requests
file_name = "batch-requests.jsonl"
requests = [
    {
        "key": "img-001",
        "request": {
            "contents": [{
                "parts": [{"text": "Professional headshot of a software engineer"}]
            }],
            "generation_config": {
                "responseModalities": ["TEXT", "IMAGE"]
            }
        }
    },
    {
        "key": "img-002",
        "request": {
            "contents": [{
                "parts": [{"text": "Mountain sunset with lake reflection"}]
            }],
            "generation_config": {
                "responseModalities": ["TEXT", "IMAGE"]
            }
        }
    }
]

with open(file_name, "w") as f:
    for req in requests:
        f.write(json.dumps(req) + "\n")

# Step 2: Upload JSONL file
uploaded_file = client.files.upload(
    file=file_name,
    config=types.UploadFileConfig(
        display_name='nanobanana-batch-requests',
        mime_type='jsonl'
    )
)
print(f"Uploaded: {uploaded_file.name}")

# Step 3: Create batch job
batch_job = client.batches.create(
    model="gemini-2.5-flash-image",
    src=uploaded_file.name,
    config={'display_name': "nanobanana-batch-001"}
)
print(f"Batch job created: {batch_job.name}")

# Step 4: Poll job status
completed_states = {'JOB_STATE_SUCCEEDED', 'JOB_STATE_FAILED',
                   'JOB_STATE_CANCELLED', 'JOB_STATE_EXPIRED'}

job = client.batches.get(name=batch_job.name)
while job.state.name not in completed_states:
    print(f"Status: {job.state.name}")
    time.sleep(10)  # Poll every 10 seconds
    job = client.batches.get(name=batch_job.name)

print(f"Job finished: {job.state.name}")

# Step 5: Download results (if successful)
if job.state.name == 'JOB_STATE_SUCCEEDED':
    result_file = job.dest.fileName
    results = client.files.download(file=result_file)

    # Step 6: Parse results JSONL
    for line in results.decode('utf-8').split('\n'):
        if line:
            response = json.loads(line)
            if 'response' in response:
                for part in response['response']['candidates'][0]['content']['parts']:
                    if 'inlineData' in part:
                        # Extract base64 image
                        image_data = part['inlineData']['data']
                        # Save to file
                        with open(f"{response['key']}.png", "wb") as f:
                            import base64
                            f.write(base64.b64decode(image_data))
```

---

## Implementation: Async Concurrent (for <10 images)

### Proper Async Pattern with Rate Limiting

```python
import asyncio
import httpx
from asyncio import Semaphore

class GeminiClient:
    def __init__(self, api_key: str, max_concurrent: int = 2):
        self.api_key = api_key
        self.semaphore = Semaphore(max_concurrent)  # Limit concurrent requests
        self.client = httpx.AsyncClient(timeout=30.0)

    async def generate_image(self, prompt: str, delay: float = 1.0):
        """
        Generate image with rate limiting and backoff

        Args:
            prompt: Text prompt for image generation
            delay: Minimum delay between requests (seconds)
        """
        async with self.semaphore:  # Acquire semaphore (max 2 concurrent)
            try:
                # Add delay to respect rate limits
                await asyncio.sleep(delay)

                response = await self.client.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent",
                    params={"key": self.api_key},
                    json={
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generation_config": {"responseModalities": ["TEXT", "IMAGE"]}
                    }
                )

                response.raise_for_status()
                return response.json()

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:  # Rate limit
                    # Exponential backoff
                    await asyncio.sleep(delay * 2)
                    return await self.generate_image(prompt, delay * 2)
                raise

    async def generate_batch(self, prompts: list[str]):
        """Generate multiple images with controlled concurrency"""
        tasks = [self.generate_image(prompt) for prompt in prompts]
        return await asyncio.gather(*tasks, return_exceptions=True)

# Usage
async def main():
    client = GeminiClient(api_key="your_key", max_concurrent=2)

    prompts = [
        "Professional headshot",
        "Mountain sunset",
        "Corporate office",
        "Beach landscape"
    ]

    results = await client.generate_batch(prompts)

    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Prompt {i} failed: {result}")
        else:
            print(f"Prompt {i} succeeded")

asyncio.run(main())
```

---

## Rate Limiting Strategy

### Free Tier Limits (Observed)

```
Individual Requests:
- Limit: ~1-2 requests per minute
- Error: 403 Forbidden after quota exhaustion
- Reset: 24 hours

Batch API:
- Limit: 1000s of requests per batch
- Turnaround: Up to 24 hours
- No immediate rate limits
```

### Recommended Strategy

**For Real-Time (<10 images)**:
```python
# Strategy 1: Sequential with delay
for prompt in prompts:
    result = await client.generate_image(prompt)
    await asyncio.sleep(30)  # Wait 30 seconds between requests

# Strategy 2: Concurrent with semaphore (max 2)
async with asyncio.Semaphore(2):
    tasks = [generate_with_delay(p, i*15) for i, p in enumerate(prompts)]
    results = await asyncio.gather(*tasks)
```

**For Background (10+ images)**:
```python
# Use Batch API
batch_job = client.batches.create(
    model="gemini-2.5-flash-image",
    src=uploaded_jsonl_file
)
# Poll every 10 seconds until complete
```

---

## Comparison Matrix

| Approach | Volume | Turnaround | Complexity | Rate Limits | Cost |
|----------|--------|------------|------------|-------------|------|
| **Sequential** | 1-5 | 3s/image | Low | ❌ Hits limits | $0.04/img |
| **Async (semaphore)** | 5-10 | 5-10s/image | Medium | ⚠️ May hit limits | $0.04/img |
| **Batch API** | 10+ | Hours | Medium | ✅ No limits | $0.04/img |

---

## NanoBanana Integration Plan

### Phase 1: Add Batch API Support (Week 2)

```python
# src/batch_generator.py
class BatchImageGenerator:
    async def generate_batch(self, requests: list[dict]) -> str:
        """
        Generate batch of images via Batch API

        Args:
            requests: List of {prompt, domain, quality} dicts

        Returns:
            batch_job_id: ID to poll for results
        """
        # 1. Create JSONL
        jsonl = self._create_jsonl(requests)

        # 2. Upload file
        file_id = await self._upload_file(jsonl)

        # 3. Create batch job
        job_id = await self._create_batch(file_id)

        return job_id

    async def poll_batch(self, job_id: str) -> list[dict]:
        """Poll batch job and return results when complete"""
        # Implementation
```

### Phase 2: Add Async Concurrent (Week 2)

```python
# src/gemini_client.py (enhancement)
class GeminiClient:
    async def generate_concurrent(
        self,
        prompts: list[str],
        max_concurrent: int = 2,
        delay_seconds: float = 15.0
    ) -> list[dict]:
        """
        Generate multiple images with controlled concurrency

        Args:
            prompts: List of prompts
            max_concurrent: Max simultaneous requests (default: 2)
            delay_seconds: Delay between request starts (default: 15s)
        """
        semaphore = asyncio.Semaphore(max_concurrent)

        async def generate_with_limit(prompt, index):
            async with semaphore:
                await asyncio.sleep(index * delay_seconds)
                return await self.generate_image(prompt)

        tasks = [generate_with_limit(p, i) for i, p in enumerate(prompts)]
        return await asyncio.gather(*tasks, return_exceptions=True)
```

### Phase 3: Smart Routing (Week 3)

```python
# src/orchestration/image_orchestrator.py
class ImageOrchestrator:
    async def generate_images(self, requests: list[dict]) -> list[dict]:
        """
        Smart routing based on volume and urgency

        Routes to:
        - Sequential: 1-3 images, real-time needed
        - Async Concurrent: 4-9 images, real-time needed
        - Batch API: 10+ images, can wait hours
        """
        if len(requests) >= 10:
            return await self.batch_generator.generate_batch(requests)
        elif len(requests) >= 4:
            return await self.gemini_client.generate_concurrent(requests)
        else:
            return await self.gemini_client.generate_sequential(requests)
```

---

## Testing Strategy

### Test 1: Batch API (10 images)
```bash
python examples/test_batch_api.py --images 10 --mode batch
# Expected: All 10 images generated in one batch job
# Turnaround: 30 minutes - 24 hours
```

### Test 2: Async Concurrent (5 images)
```bash
python examples/test_concurrent.py --images 5 --concurrent 2 --delay 15
# Expected: 5 images in ~1-2 minutes
# Rate limit: Should not hit 403 errors
```

### Test 3: Sequential (3 images)
```bash
python examples/test_sequential.py --images 3 --delay 30
# Expected: 3 images in ~1.5 minutes
# Rate limit: Should not hit 403 errors
```

---

## Production Recommendations

1. **Use Batch API for Background Jobs**
   - Any request for 10+ images
   - Non-urgent generation requests
   - Scheduled bulk generation

2. **Use Async Concurrent for Interactive**
   - 4-9 images with user waiting
   - Real-time generation needed
   - Max 2 concurrent requests with 15s delay

3. **Use Sequential for Small Requests**
   - 1-3 images
   - Immediate response needed
   - 30 second delay between requests

4. **Implement Circuit Breaker**
   - After 3 consecutive 403 errors, switch to Batch API
   - Prevent wasting quota on failing requests

5. **Monitor Quota Usage**
   - Track successful vs failed requests
   - Alert when approaching daily limits
   - Implement graceful degradation

---

## Next Steps

1. ✅ Research complete - Batch API documented
2. ⏳ Implement batch generator class (4 hours)
3. ⏳ Add async concurrent support (3 hours)
4. ⏳ Create smart routing logic (2 hours)
5. ⏳ Write comprehensive tests (3 hours)
6. ⏳ Update Flask API to support batch mode (2 hours)

**Total Estimated Time**: 14 hours (Week 2 priority)

---

**Status**: ✅ **RESEARCH COMPLETE - READY FOR IMPLEMENTATION**
**Priority**: High (prevents rate limit failures)
**ROI**: Eliminates 80-90% failure rate, enables scaling to 1000+ images
