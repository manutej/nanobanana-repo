# NanoBanana Refactoring - Quick Reference Card

**Print this. Pin it to your wall. Keep it handy.**

---

## Week 1 Checklist (17 hours)

### ✅ Day 1: Error Handling (2h)
- [ ] Create `src/api/error_handler.py`
- [ ] Define `APIError`, `ValidationError`, `ExternalServiceError`
- [ ] Create `@handle_api_errors` decorator
- [ ] Add decorator to all routes in `main.py`
- [ ] Test: Invalid requests return 400, API failures return 502

### ✅ Day 2: Logging (2h)
- [ ] Create `config/logging_config.py`
- [ ] Define `JSONFormatter` class
- [ ] Replace all `print()` with `logger.info/warning/error()`
- [ ] Add `extra={}` fields for structured data
- [ ] Test: Logs are JSON, include context (domain, model, etc.)

### ✅ Day 3: Configuration (3h)
- [ ] Create `config/settings.py` with `Settings` dataclass
- [ ] Create `.env.example` with all variables
- [ ] Update `main.py` to use `settings` object
- [ ] Validate settings on startup
- [ ] Test: App fails fast if API key missing

### ✅ Day 4-5: Tests (6h)
- [ ] Create `tests/test_critical_paths.py`
- [ ] Write `test_classify_accuracy()` with 6 test cases
- [ ] Write `test_template_enhancement()` (basic/detailed/expert)
- [ ] Write `test_gemini_retry_logic()` (mocked failures)
- [ ] Write `test_happy_path()` (end-to-end)
- [ ] Test: `pytest tests/ -v` passes with 80%+ coverage

### ✅ Day 6: Service Layer (4h)
- [ ] Create `src/services/image_service.py`
- [ ] Define `ImageGenerationService` class
- [ ] Implement `generate_image()`, `classify_prompt()`, `enhance_prompt()`
- [ ] Update `main.py` routes to call service (not orchestrate)
- [ ] Test: Service works independently of Flask

---

## Week 2 Checklist (6.5 hours)

### ✅ External Configs (2h)
- [ ] Create `config/domains.yaml`
- [ ] Move `DOMAIN_KEYWORDS` from code to YAML
- [ ] Update `DomainClassifier.__init__()` to load YAML
- [ ] Test: Add new domain via YAML (no code change)

### ✅ Shared Matcher (1.5h)
- [ ] Create `src/core/keyword_matcher.py`
- [ ] Define `KeywordMatcher.score_matches()`
- [ ] Replace duplicate logic in `domain_classifier.py`
- [ ] Replace duplicate logic in `template_engine.py`
- [ ] Test: Classification still works

### ✅ Classifier Interface (3h)
- [ ] Create `src/core/classifier_interface.py` (ABC)
- [ ] Rename `DomainClassifier` → `KeywordClassifier`
- [ ] Make `KeywordClassifier` implement interface
- [ ] Update `main.py` to use interface
- [ ] Test: Can swap classifier implementations

---

## Command Cheat Sheet

### Development
```bash
# Start server
python src/main.py

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=src --cov-report=term-missing

# Format code
black src/ tests/

# Type check
mypy src/

# Lint
pylint src/
```

### Testing Endpoints
```bash
# Generate image
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "CEO headshot", "quality": "expert"}'

# Classify prompt
curl -X POST http://localhost:8080/classify \
  -H "Content-Type: application/json" \
  -d '{"prompt": "AWS architecture diagram"}'

# Enhance prompt
curl -X POST http://localhost:8080/enhance \
  -H "Content-Type: application/json" \
  -d '{"prompt": "sunset", "quality": "detailed"}'

# Health check
curl http://localhost:8080/health
```

---

## Code Snippets (Copy-Paste)

### Error Handler Decorator
```python
from functools import wraps
from flask import jsonify

def handle_api_errors(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationError as e:
            logger.warning(f"Validation: {e.message}")
            return jsonify({"error": e.message}), 400
        except Exception as e:
            logger.exception(f"Error: {e}")
            return jsonify({"error": "Internal error"}), 500
    return decorated
```

### Structured Logging
```python
from config.logging_config import get_logger

logger = get_logger(__name__)

logger.info(
    "Image generated",
    extra={
        "domain": domain,
        "model": model,
        "size_bytes": len(image_data)
    }
)
```

### Settings Usage
```python
from config.settings import settings

# Validate on startup
settings.validate()

# Use in code
api_key = settings.google_api_key
default_model = settings.default_model
```

### Service Layer
```python
from services.image_service import ImageGenerationService

service = ImageGenerationService(
    classifier=classifier,
    template_engine=template_engine,
    gemini_client_factory=lambda: GeminiClient()
)

# In route
result = run_async(service.generate_image(
    prompt=data["prompt"],
    quality=data.get("quality", "detailed"),
    model=data.get("model", "flash")
))
```

### Test Example
```python
@pytest.mark.parametrize("prompt,expected_domain", [
    ("CEO headshot", "photography"),
    ("AWS diagram", "diagrams"),
])
def test_classify(prompt, expected_domain):
    classifier = DomainClassifier()
    domain, _ = classifier.classify_with_confidence(prompt)
    assert domain == expected_domain
```

---

## File Locations Quick Map

```
src/
├── api/
│   └── error_handler.py          ← Day 1
├── services/
│   └── image_service.py          ← Day 6
├── core/
│   ├── classifier_interface.py   ← Week 2
│   └── keyword_matcher.py        ← Week 2
└── main.py                       ← Update Days 1, 3, 6

config/
├── logging_config.py             ← Day 2
├── settings.py                   ← Day 3
└── domains.yaml                  ← Week 2

tests/
└── test_critical_paths.py        ← Days 4-5

.env.example                      ← Day 3
```

---

## Decision Flowchart

```
New feature needed?
    │
    ├─► Can I do it with YAML change?
    │   └─► Yes → Edit YAML, test, deploy ✅
    │   └─► No → Continue
    │
    ├─► Does it fit existing ContentType?
    │   └─► Yes → Add to service layer ✅
    │   └─► No → New ContentType needed
    │
    └─► New ContentType
        └─► Implement ContentGenerator interface
        └─► Register in orchestrator
        └─► Deploy ✅

Bug found?
    │
    ├─► Is there a test for it?
    │   └─► No → Write test first ✅
    │   └─► Yes → Continue
    │
    ├─► Fix bug
    ├─► Verify test passes
    └─► Deploy ✅

Refactor idea?
    │
    ├─► Is it causing pain? (bugs, slow dev)
    │   └─► No → Skip (YAGNI)
    │   └─► Yes → Continue
    │
    ├─► Will it block new features?
    │   └─► No → Low priority
    │   └─► Yes → High priority
    │
    ├─► Do I have tests?
    │   └─► No → Write tests first
    │   └─► Yes → Continue
    │
    ├─► Refactor
    ├─► Tests still pass?
    │   └─► No → Revert, fix
    │   └─► Yes → Commit ✅
```

---

## Metrics to Track

### Before Refactoring (Baseline)
- Time to add new feature: _____ hours
- Deployment confidence: _____%
- Bug rate (bugs/week): _____
- Time to debug production issue: _____ hours

### After Week 1
- Time to add new feature: _____ hours (target: -50%)
- Deployment confidence: ____% (target: 90%+)
- Test coverage: ____% (target: 80%+)
- Time to debug: _____ hours (target: -70%)

### After Week 2
- Time to add new domain: _____ minutes (target: <15 min)
- Code duplication: ____% (target: <5%)
- Service reuse: _____ places (CLI, workers, etc.)

---

## Common Pitfalls

### ❌ Don't Do This
```python
# Mixing HTTP and business logic
@app.route("/generate")
def generate():
    # 100 lines of business logic here
    domain = classifier.classify(...)
    enhanced = template_engine.enhance(...)
    # ...
```

### ✅ Do This Instead
```python
# Clean separation
@app.route("/generate")
@handle_api_errors
def generate():
    data = require_json_field(request, "prompt")
    result = run_async(service.generate_image(**data))
    return jsonify(result), 200
```

---

### ❌ Don't Do This
```python
# Print debugging
print(f"Domain: {domain}")
print(f"ERROR: {e}")
```

### ✅ Do This Instead
```python
# Structured logging
logger.info("Domain classified", extra={"domain": domain})
logger.error("API call failed", extra={"error": str(e)})
```

---

### ❌ Don't Do This
```python
# Hard-coded config
if quality not in ["basic", "detailed", "expert"]:
    raise ValueError("Invalid quality")
```

### ✅ Do This Instead
```python
# Settings-driven
if quality not in settings.valid_qualities:
    raise ValidationError(f"Invalid quality: {quality}")
```

---

### ❌ Don't Do This
```python
# Untested code
def new_feature():
    # ... complex logic ...
    return result
```

### ✅ Do This Instead
```python
# Test first
def test_new_feature():
    result = new_feature(test_input)
    assert result == expected_output

def new_feature():
    # ... complex logic ...
    return result
```

---

## Emergency Shortcuts

### "I only have 2 hours!"
Do this subset:
1. ✅ Error handler decorator (1h)
2. ✅ Replace print with logging (1h)

**Impact**: 60% of value, 10% of effort

---

### "I need to ship today!"
Skip refactoring, but:
1. ✅ Write 1 test for your change (15 min)
2. ✅ Check logs are structured (5 min)
3. ✅ Verify error handling works (5 min)

**Impact**: Ship confidently, refactor later

---

### "Production is broken!"
Debug with structured logs:
```bash
# If using JSON logs
cat logs.json | jq '.level == "ERROR"'

# Find specific error
cat logs.json | jq '.message | contains("API call failed")'

# Get context
cat logs.json | jq 'select(.request_id == "abc123")'
```

---

## Remember

### The Pragmatic Way
1. **Care about your craft** - Write code you're proud of
2. **Think critically** - Question "we've always done it this way"
3. **Take ownership** - It's your code, your responsibility
4. **Provide options** - Solutions, not excuses
5. **Invest in knowledge** - Learn continuously
6. **Delight users** - Value over code
7. **Have fun** - Enjoy the craft

### The Pragmatic Priorities
1. **Does it solve a real problem?** If no, skip it
2. **Will it prevent future bugs?** High priority
3. **Does it make adding features easier?** High priority
4. **Is it just "theoretically better"?** Low priority

### The Pragmatic Test
**Before refactoring, ask:**
- Will this make my life easier in 2 weeks?
- Will this prevent a class of bugs?
- Will this speed up development?

**If "no" to all three → Skip it (YAGNI)**

---

## One-Liner Rules

1. **DRY**: If you copy-paste 3+ times, extract a function
2. **KISS**: Simple code > clever code
3. **YAGNI**: Don't build for imaginary future requirements
4. **Tests**: If you can't test it, refactor it
5. **Errors**: Log structured data, not print statements
6. **Config**: Move hard-coded values to settings/YAML
7. **Separation**: HTTP layer ≠ Business layer ≠ Data layer

---

## Success Criteria

### Week 1 Done When:
- [ ] All routes use `@handle_api_errors`
- [ ] No `print()` statements (only `logger.*()`)
- [ ] Settings load from `.env`
- [ ] 5+ tests pass with 80%+ coverage
- [ ] Service layer extracts business logic

### Week 2 Done When:
- [ ] Domains load from `domains.yaml`
- [ ] No duplicate keyword matching logic
- [ ] Classifier implements interface
- [ ] Can add new domain via YAML (test it!)

### Production Ready When:
- [ ] Tests pass
- [ ] Logs are structured JSON
- [ ] Settings validated on startup
- [ ] Error handling consistent
- [ ] Deployment confidence >90%

---

## Help Shortcuts

| Problem | Document | Section |
|---------|----------|---------|
| **What to do first?** | CODE-REVIEW-SUMMARY.md | TL;DR |
| **How to implement X?** | REFACTORING-GUIDE.md | Find day/section |
| **Why this refactor?** | PRAGMATIC-CODE-REVIEW.md | Find issue # |
| **Visual architecture** | ARCHITECTURE-COMPARISON.md | Diagrams |
| **Navigation** | INDEX.md | Reading paths |

---

**Print this card. Keep it visible. Reference daily.**

*"Good enough for now, easy to improve later"*
