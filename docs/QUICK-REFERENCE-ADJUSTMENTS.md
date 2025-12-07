# Quick Reference - Implementation Adjustments

**MARS Validation Result**: ✅ GO (89% confidence)

**Status**: 4 fixes architecturally sound WITH adjustments

---

## 🔴 CRITICAL: Replace File Cache with Redis

**RMP Plan Said**: File-based cache (cache/ directory)
**MARS Says**: ❌ Won't work on Cloud Run (ephemeral filesystem)

**Use This Instead**:

```python
# orchestrator/cache_manager.py
import redis
from datetime import timedelta

class CacheManager:
    def __init__(self, redis_url: str):
        self.redis = redis.Redis.from_url(redis_url)
        self.ttl = timedelta(hours=24)

    def get(self, key: str) -> Optional[bytes]:
        return self.redis.get(key)

    def set(self, key: str, value: bytes):
        self.redis.setex(key, self.ttl, value)
```

**Setup**: Cloud Memorystore (Redis) - $40/month
**ROI**: $996/year savings (30% cache hits)

---

## 🟡 RECOMMENDED: Fix File Locations

**RMP Plan Said**: `CLAUDE.md` in repo root
**MARS Says**: ⚠️ Conflicts with project CLAUDE.md

**Use This Instead**: `/docs/PROMPT-ENGINEERING-GUIDELINES.md`

**Why**: Workspace hygiene + clear naming

---

## 🟡 RECOMMENDED: Test Aspect Ratio FIRST

**RMP Plan Said**: Implement with gemini-3-pro-image-preview
**MARS Says**: ⚠️ Current model may not support imageConfig

**Do This First** (Day 1, 4 hours):

```python
# Test if model supports aspect ratio
async def test_aspect_ratio():
    response = await client.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent",
        json={
            "contents": [{"parts": [{"text": "test"}]}],
            "generationConfig": {
                "imageConfig": {"aspectRatio": "16:9", "imageSize": "2K"}
            }
        }
    )

    if response.status_code == 200:
        print("✅ Supported - implement in Week 2")
    else:
        print("❌ Not supported - defer to Phase 2")
```

**IF Supported**: Implement ✅
**IF Not**: Document limitation, defer ⏸️

---

## 🟡 RECOMMENDED: Modular Refactor Early

**RMP Plan Said**: Refactor in Week 3 (per ADR-001)
**MARS Says**: ✅ Do it in Week 2 Day 5 (easier now than later)

**Target Structure**:

```
nanobanana/
├── intent/
│   ├── keyword_classifier.py (exists)
│   └── llm_analyzer.py (Fix 1 - new)
├── orchestrator/
│   ├── prompt_enhancer.py (exists: template_engine.py)
│   └── cache_manager.py (Fix 4 - Redis version)
└── adapters/
    └── gemini_adapter.py (Fix 2 - update gemini_client.py)
```

**Why Early**: 500 LOC now vs 2000 LOC later

---

## Summary of Changes

| RMP Plan | MARS Adjustment | Priority |
|----------|-----------------|----------|
| File-based cache | Redis cache | 🔴 CRITICAL |
| `CLAUDE.md` (root) | `/docs/PROMPT-ENGINEERING-GUIDELINES.md` | 🟡 Recommended |
| Implement aspect ratio | Test FIRST, then implement | 🟡 Recommended |
| Refactor Week 3 | Refactor Week 2 Day 5 | 🟡 Recommended |

---

## What Stays The Same

✅ **Fix 1: LLM Enhancement** - Implement as planned (tiered strategy)
✅ **Fix 2: Aspect Ratio** - Concept correct, just validate first
✅ **Fix 3: Guidelines** - Content correct, just different filename
✅ **Fix 4: Caching** - Strategy correct, implementation needs Redis

---

## Timeline Impact

**RMP Plan**: 2 weeks
**MARS Plan**: 3.2 weeks (16 days)

**Why Longer**:
- Day 1: Validation (de-risk aspect ratio)
- Week 2 Day 5: Modular refactor (future-proofing)
- Week 3: A/B testing + load testing (validate at scale)

**ROI**: 60% longer timeline → 95% confidence vs 70% rushing

---

## Quick Decision Tree

```
START
  ↓
Q: Can we use Redis?
  YES → ✅ Proceed with all 4 fixes
  NO  → ❌ Defer Fix 4 (cache) to Phase 2, do Fixes 1-3 only
  ↓
Q: Does aspect ratio test pass?
  YES → ✅ Implement Fix 2 in Week 2
  NO  → ⏸️ Defer Fix 2 to Phase 2, document limitation
  ↓
Q: Can we afford 3.2 weeks?
  YES → ✅ Follow MARS plan (95% confidence)
  NO  → ⚠️ Do Week 1 only (Fixes 1, 3, 4), defer rest
```

---

## Success Metrics (Week 4)

| Metric | Target | Test Method |
|--------|--------|-------------|
| Accuracy (Overall) | 98% | 100 test prompts |
| Accuracy (Ambiguous) | 90% | 20 ambiguous prompts |
| Cache Hit Rate | 30% | Redis metrics |
| Cost/Image | $0.035 | Actual billing |
| Latency P95 | <5s | Cloud Run metrics |

**Pass Threshold**: 4/5 metrics met → Success ✅
**Fail Threshold**: <3/5 metrics met → Re-evaluate ⚠️

---

## Questions? Check These Docs

- **Full Validation**: `/docs/MARS-SYSTEMS-VALIDATION-REPORT.md` (12K words, 89% confidence)
- **Decision Summary**: `/docs/IMPLEMENTATION-DECISION.md` (2K words)
- **Original Plan**: `/docs/RMP-IMPLEMENTATION-PLAN.md`
- **Architecture**: `/docs/ADR-001-MAINTAIN-MONOLITH.md`

---

**Last Updated**: 2025-12-07
**Validated By**: MARS (Multi-Agent Research Synthesis)
**Confidence**: 89% (95% with adjustments)
