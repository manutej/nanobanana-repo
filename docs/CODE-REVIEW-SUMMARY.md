# NanoBanana Code Review - Executive Summary

**Date**: 2025-12-07
**Current Quality**: 7/10
**Target Quality**: 9/10 (after high-priority fixes)

---

## TL;DR - What to Do Now

### Week 1: Foundation (17 hours)
1. **Centralized error handling** (2h) - Stop repeating try/except
2. **Structured logging** (2h) - Replace print with JSON logs
3. **Configuration management** (3h) - Move settings to .env + YAML
4. **Integration tests** (6h) - Write 5-10 critical path tests
5. **Service layer extraction** (4h) - Separate business logic from Flask

### Week 2: Extensibility (8 hours)
1. **External domain configs** (2h) - YAML instead of hard-coded dicts
2. **Shared keyword matcher** (1.5h) - Fix DRY violation
3. **Classifier interface** (3h) - Prepare for LLM classifier swap

**Total Time**: 25 hours (1 sprint)
**Impact**: Production-ready, testable, extensible codebase

---

## Current Issues (Top 5)

| Priority | Issue | Impact | Effort |
|----------|-------|--------|--------|
| 🔴 High | No error handling consistency | Hard to debug production | 2h |
| 🔴 High | Print instead of logging | Can't query logs | 2h |
| 🔴 High | No tests | Fear of breaking things | 6h |
| 🔴 High | Hard-coded domains | Can't add new types easily | 2h |
| 🟡 Medium | Business logic in routes | Can't reuse or test | 4h |

---

## Code Quality Metrics

### Before Refactoring
- ✅ **Modularity**: 8/10 - Good separation already
- ❌ **Testability**: 2/10 - No tests, hard to mock
- ⚠️ **Maintainability**: 6/10 - Will decay over time
- ✅ **Readability**: 8/10 - Clean, well-documented
- ❌ **Observability**: 3/10 - Print statements only
- ⚠️ **Extensibility**: 5/10 - Hard-coded configurations

### After High-Priority Fixes
- ✅ **Modularity**: 9/10
- ✅ **Testability**: 8/10 - Full test coverage
- ✅ **Maintainability**: 9/10 - Easy to change
- ✅ **Readability**: 9/10
- ✅ **Observability**: 9/10 - Structured logs
- ✅ **Extensibility**: 8/10 - Config-driven

---

## Files to Create

```
nanobanana-repo/
├── config/
│   ├── settings.py          # NEW - Settings dataclass
│   ├── logging_config.py    # NEW - Structured logging
│   └── domains.yaml         # NEW - Domain keywords
├── src/
│   ├── api/
│   │   └── error_handler.py # NEW - Centralized errors
│   └── services/
│       └── image_service.py # NEW - Business logic
└── tests/
    └── test_critical_paths.py # NEW - Integration tests
```

**Total New Code**: ~800 lines
**Modified Code**: ~100 lines
**Deleted Code**: ~50 lines (duplicates removed)

---

## Quick Wins (Do First)

### 1-Hour Tasks
- [ ] Replace `print()` with `logger.info()` (30 min)
- [ ] Create `.env.example` file (15 min)
- [ ] Add type hints to functions (1 hour)

### 2-Hour Tasks
- [ ] Centralized error handling decorator (2h)
- [ ] Configuration YAML files (2h)
- [ ] Write first 3 tests (2h)

---

## Code Examples

### Before: Duplicated Error Handling
```python
# main.py - 4 routes with identical error handling
try:
    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "Missing prompt"}), 400
    # ... logic ...
except ValueError as e:
    return jsonify({"error": str(e)}), 400
except Exception as e:
    print(f"ERROR: {e}")
    return jsonify({"error": "Internal error"}), 500
```

### After: DRY with Decorator
```python
# api/error_handler.py
def handle_api_errors(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"Validation: {e}")
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.exception(f"Error: {e}")
            return jsonify({"error": "Internal error"}), 500
    return decorated

# main.py - Clean routes
@app.route("/generate", methods=["POST"])
@handle_api_errors  # <-- Magic!
def generate_image():
    data = require_json_field(request, "prompt")
    # ... clean logic, no try/except ...
```

**Savings**: 20 lines of duplicated code removed

---

### Before: Business Logic in Route
```python
@app.route("/generate", methods=["POST"])
def generate_image():
    # 110 lines of:
    # - Request validation
    # - Domain classification
    # - Template enhancement
    # - API calls
    # - Response formatting
    # - Error handling
```

### After: Service Layer
```python
# services/image_service.py
class ImageGenerationService:
    async def generate_image(self, prompt, quality, model):
        # 30 lines of pure business logic
        # No HTTP, no Flask, no JSON
        # Easy to test!

# main.py
@app.route("/generate", methods=["POST"])
@handle_api_errors
def generate_image():
    data = require_json_field(request, "prompt")
    result = run_async(image_service.generate_image(
        prompt=data["prompt"],
        quality=data.get("quality", "detailed"),
        model=data.get("model", "flash")
    ))
    return format_response(result), 200
```

**Benefits**:
- ✅ Testable without Flask
- ✅ Reusable in CLI, workers, etc.
- ✅ Clear separation of concerns

---

### Before: Hard-Coded Configuration
```python
# domain_classifier.py
DOMAIN_KEYWORDS = {
    "photography": ["photo", "portrait", ...],
    "diagrams": ["diagram", "chart", ...],
    # ... 50 lines of keywords
}
```

**Problem**: Adding new domain requires code change + deployment

### After: External Configuration
```yaml
# config/domains.yaml
domains:
  photography:
    keywords: [photo, portrait, headshot, ...]
  diagrams:
    keywords: [diagram, chart, flowchart, ...]
  presentations:  # NEW - Just edit YAML!
    keywords: [slide, deck, powerpoint, ...]
```

```python
# domain_classifier.py
def __init__(self, config_path="config/domains.yaml"):
    with open(config_path) as f:
        config = yaml.safe_load(f)
    self.DOMAIN_KEYWORDS = {
        d: data["keywords"]
        for d, data in config["domains"].items()
    }
```

**Benefits**:
- ✅ Add domains without code changes
- ✅ A/B test different keyword sets
- ✅ Environment-specific configs

---

## Testing Strategy

### Don't Write
- ❌ 100 unit tests for every function
- ❌ Tests for trivial getters/setters
- ❌ Tests that just call the real API

### Do Write
- ✅ 5-10 integration tests for critical paths
- ✅ Tests for domain classification accuracy
- ✅ Tests for error handling (retry, timeout)
- ✅ Tests with mocked Gemini API

**Example**:
```python
def test_happy_path():
    """End-to-end: prompt → classify → enhance → generate"""
    prompt = "professional CEO headshot"

    # Classify
    domain, confidence = classifier.classify(prompt)
    assert domain == "photography"

    # Enhance
    enhanced = template_engine.enhance(prompt, domain, "expert")
    assert "Phase One" in enhanced  # Expert specs

    # Generate (mocked)
    with mock_gemini_api():
        result = client.generate_image(enhanced)
        assert len(result["image_data"]) > 0
```

**Coverage Goal**: 80% of critical paths, not 100% line coverage

---

## Meta-Prompting Preparation

### Current State
- ✅ `llm_prompt_enhancer.py` exists
- ❌ Not integrated into main flow
- ❌ No quality gates
- ❌ No caching

### Pragmatic Integration
```python
# services/meta_prompter.py
class MetaPrompter:
    async def enhance(self, prompt: str, max_depth: int = 2):
        """Recursively improve prompt until quality threshold."""
        if depth >= max_depth:
            return prompt  # Stop

        enhanced = await llm_enhancer.enhance_prompt(prompt)
        quality = await self._evaluate_quality(enhanced)

        if quality >= 0.8:
            return enhanced  # Good enough

        return await self.enhance(enhanced, depth + 1)  # Recurse
```

**Design Decisions**:
- **Infinite loop prevention**: Max depth = 2
- **When to stop**: Quality threshold (0.8) OR max depth
- **Which model**: Gemini (already integrated)
- **Cost control**: LRU cache (1000 entries)

---

## Evolution Roadmap

### Phase 1: Stabilize (Weeks 1-2)
- Error handling
- Logging
- Configuration
- Tests

**Outcome**: Production-ready monolith

### Phase 2: Extract (Weeks 3-4)
- Service layer
- Classifier interface
- Content type abstraction

**Outcome**: Pluggable architecture

### Phase 3: Extend (Weeks 5-8)
- Presentations
- UI components
- Diagrams
- Videos

**Outcome**: Multi-media factory

### Phase 4: Optimize (Weeks 9-12)
- Meta-prompting
- LLM enhancement
- A/B testing

**Outcome**: Intelligent prompt optimization

---

## Resources

### Documentation
- **PRAGMATIC-CODE-REVIEW.md** - Complete 13-section analysis (20 pages)
- **REFACTORING-GUIDE.md** - Step-by-step implementation (15 pages)
- **This Summary** - Quick reference

### Key Files
```bash
# Read these first
docs/PRAGMATIC-CODE-REVIEW.md      # Deep analysis
docs/REFACTORING-GUIDE.md          # Implementation guide
docs/CODE-REVIEW-SUMMARY.md        # This file

# Core code to refactor
src/main.py                        # Flask routes (God object)
src/domain_classifier.py           # Hard-coded keywords
src/template_engine.py             # Subcategory keywords
src/gemini_client.py              # Print → logging
```

---

## Decision Matrix

### Should I Refactor This?

Ask these questions:

1. **Is it causing pain?**
   - ✅ Yes → High priority
   - ❌ No → Low priority

2. **Will it block new features?**
   - ✅ Yes → High priority
   - ❌ No → Medium priority

3. **Is it violating Rule of Three?**
   - ✅ 3+ duplicates → Refactor
   - ❌ 1-2 occurrences → Wait

4. **Can I write a test for it?**
   - ❌ No → Refactor for testability
   - ✅ Yes → Write test first

### Priority Formula
```
Priority = (Pain × 3) + (Blocks Features × 2) + (DRY Violations × 1)

High:   Score ≥ 8
Medium: Score 4-7
Low:    Score ≤ 3
```

---

## Final Recommendation

### Do This Week
1. ✅ Centralized error handling (2h)
2. ✅ Structured logging (2h)
3. ✅ Configuration management (3h)

**Total**: 7 hours
**Impact**: Deployable, debuggable

### Do Next Week
1. ✅ Integration tests (6h)
2. ✅ Service layer extraction (4h)
3. ✅ External domain configs (2h)

**Total**: 12 hours
**Impact**: Testable, extensible

### Do Later
- Meta-prompting (8h)
- New content types (16h)
- A/B testing (8h)

---

## Questions?

**"Should I refactor everything now?"**
No. High-priority fixes first (17 hours). Ship. Iterate.

**"What if I don't have 17 hours?"**
Start with 7-hour subset (error handling + logging + config). Still valuable.

**"How do I know if refactoring worked?"**
Measure: time to add new feature, bug rate, deployment frequency

**"What's the one thing to do first?"**
Centralized error handling (2h). Biggest pain relief per hour.

---

**Status**: Ready for implementation ✅
**Next Step**: Copy code from REFACTORING-GUIDE.md and start coding

*Good luck, and remember: "Good enough for now, easy to improve later"*
