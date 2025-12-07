# NanoBanana Architecture Comparison

**Visual guide**: Current monolith → Refactored service layer → Future multi-media factory

---

## Current Architecture (Monolith)

```
┌─────────────────────────────────────────────────────────────┐
│                         main.py                             │
│                      (350 lines)                            │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Flask Routes (HTTP Layer)                           │  │
│  │  • /generate                                         │  │
│  │  • /classify                                         │  │
│  │  • /enhance                                          │  │
│  │  • /health                                           │  │
│  └───────────┬──────────────────────────────────────────┘  │
│              │                                              │
│  ┌───────────▼──────────────────────────────────────────┐  │
│  │  Orchestration Logic (Business Layer)                │  │
│  │  • Request validation                                │  │
│  │  • Domain classification                             │  │
│  │  • Template enhancement                              │  │
│  │  • API calls                                         │  │
│  │  • Error handling (try/except everywhere)            │  │
│  └───────────┬──────────────────────────────────────────┘  │
│              │                                              │
│  ┌───────────▼──────────────────────────────────────────┐  │
│  │  Response Formatting                                 │  │
│  │  • JSON serialization                                │  │
│  │  • Base64 encoding                                   │  │
│  │  • Metadata construction                             │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

┌──────────────────┐   ┌────────────────┐   ┌──────────────┐
│ domain_classifier│   │template_engine │   │gemini_client │
│                  │   │                │   │              │
│ Hard-coded       │   │ Hard-coded     │   │ Async HTTP   │
│ DOMAIN_KEYWORDS  │   │ subcategory    │   │ + Retry      │
│ dict             │   │ keywords       │   │              │
└──────────────────┘   └────────────────┘   └──────────────┘
```

### Problems
- ❌ **God Object**: main.py does everything
- ❌ **Tight Coupling**: HTTP + business logic + formatting mixed
- ❌ **Hard to Test**: Must mock Flask request/response
- ❌ **Hard to Reuse**: Can't use logic outside Flask
- ❌ **Hard-Coded Config**: Adding domains requires code change

---

## Refactored Architecture (Service Layer)

```
┌─────────────────────────────────────────────────────────────┐
│                      Flask Layer                            │
│                     (main.py - 150 lines)                   │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Routes (HTTP Adapter)                               │  │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐     │  │
│  │  │generate│  │classify│  │enhance │  │ health │     │  │
│  │  └────┬───┘  └────┬───┘  └────┬───┘  └────┬───┘     │  │
│  │       │           │           │           │          │  │
│  │       │     ┌─────▼───────────▼───────────▼────┐     │  │
│  │       │     │  Request Validation              │     │  │
│  │       │     │  (validators.py)                 │     │  │
│  │       │     └──────────────────────────────────┘     │  │
│  └───────┼──────────────────────────────────────────────┘  │
│          │                                                  │
│  ┌───────▼──────────────────────────────────────────────┐  │
│  │  Error Handler (decorator)                           │  │
│  │  • ValidationError → 400                             │  │
│  │  • ExternalServiceError → 502                        │  │
│  │  • Exception → 500                                   │  │
│  │  • Structured logging                                │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Calls
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  Service Layer                              │
│               (services/image_service.py)                   │
│                  Framework-Agnostic                         │
│                                                             │
│  class ImageGenerationService:                             │
│                                                             │
│    async def generate_image(prompt, quality, model):       │
│      1. domain, confidence = classifier.classify(prompt)   │
│      2. subcategory = template_engine.suggest(prompt)      │
│      3. enhanced = template_engine.enhance(...)            │
│      4. result = await gemini_client.generate(enhanced)    │
│      return structured_data (not HTTP response!)           │
│                                                             │
│    async def classify_prompt(prompt): ...                  │
│    async def enhance_prompt(prompt): ...                   │
│                                                             │
└────────────┬─────────────┬──────────────┬───────────────────┘
             │             │              │
        ┌────▼───┐   ┌─────▼────┐   ┌────▼────┐
        │        │   │          │   │         │
┌───────▼──────┐ │   │ ┌────────▼─────┐ │   │ ┌──────▼──────┐
│ Classifier   │ │   │ │Template      │ │   │ │Gemini       │
│ Interface    │ │   │ │Engine        │ │   │ │Client       │
│ (ABC)        │ │   │ │              │ │   │ │             │
│              │ │   │ │ Loads        │ │   │ │ Circuit     │
│ ┌──────────┐ │ │   │ │ templates    │ │   │ │ Breaker     │
│ │Keyword   │◄┘ │   │ │ from JSON    │ │   │ │             │
│ │Classifier│   │   │ └──────────────┘ │   │ │ Retry       │
│ │          │   │   │                  │   │ │ Logic       │
│ │Loads from│   │   │                  │   │ │             │
│ │YAML      │   │   │                  │   │ └─────────────┘
│ └──────────┘   │   │                  │   │
│                │   │                  │   │
│ ┌──────────┐   │   │                  │   │
│ │LLM       │   │   │                  │   │
│ │Classifier│◄──┘   │                  │   │
│ │(future)  │       │                  │   │
│ └──────────┘       │                  │   │
└────────────────────┘                  └───┘
         ▲
         │
┌────────▼─────────┐
│ config/          │
│ domains.yaml     │
│                  │
│ domains:         │
│   photography:   │
│     keywords: [] │
│   diagrams: ...  │
└──────────────────┘
```

### Benefits
- ✅ **Separation of Concerns**: HTTP ≠ Business Logic ≠ External APIs
- ✅ **Testable**: Service layer has no Flask dependencies
- ✅ **Reusable**: Use service in CLI, workers, Lambda functions
- ✅ **Pluggable**: Swap keyword classifier for LLM classifier
- ✅ **Config-Driven**: Add domains via YAML, not code

---

## Future Architecture (Multi-Media Factory)

```
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway                            │
│                     (main.py)                               │
│                                                             │
│  Routes:                                                    │
│  /generate/{content_type}                                   │
│    • images                                                 │
│    • presentations                                          │
│    • ui-components                                          │
│    • diagrams                                               │
│    • videos                                                 │
│                                                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │
┌────────────────────────▼────────────────────────────────────┐
│              Content Generation Orchestrator                │
│            (services/content_orchestrator.py)               │
│                                                             │
│  async def generate_content(                                │
│      prompt: str,                                           │
│      content_type: ContentType,                             │
│      quality: str,                                          │
│      meta_prompting: bool = False                           │
│  ):                                                         │
│      1. Classify content type (if auto-detect)             │
│      2. Enhance prompt (template OR meta-prompting)        │
│      3. Route to appropriate generator                     │
│      4. Return multi-format result                         │
│                                                             │
└───┬────────┬───────────┬───────────┬────────────┬───────────┘
    │        │           │           │            │
┌───▼──┐ ┌───▼──┐ ┌──────▼─┐ ┌───────▼──┐ ┌──────▼────┐
│Image │ │Pres- │ │   UI   │ │ Diagram  │ │  Video    │
│Gen   │ │enta- │ │  Comp  │ │   Gen    │ │   Gen     │
│      │ │tion  │ │   Gen  │ │          │ │           │
│      │ │      │ │        │ │          │ │           │
│Gemini│ │Google│ │ Figma  │ │Excalidraw│ │  RunwayML │
│Image │ │Slides│ │  API   │ │  Mermaid │ │   API     │
│API   │ │ API  │ │        │ │          │ │           │
└──────┘ └──────┘ └────────┘ └──────────┘ └───────────┘

         All implement ContentGenerator interface:
         ┌────────────────────────────────────────┐
         │ class ContentGenerator(ABC):           │
         │   @abstractmethod                      │
         │   async def generate(prompt) -> bytes  │
         │                                        │
         │   @abstractmethod                      │
         │   def supports_quality() -> bool       │
         │                                        │
         │   @abstractmethod                      │
         │   def get_formats() -> List[str]       │
         └────────────────────────────────────────┘
```

### Meta-Prompting Integration

```
┌─────────────────────────────────────────────────────────────┐
│              Prompt Enhancement Pipeline                    │
│                                                             │
│  User Prompt                                                │
│      │                                                      │
│      ▼                                                      │
│  ┌────────────────────────────┐                            │
│  │  Enhancement Router        │                            │
│  │  (decides: template vs LLM)│                            │
│  └──┬─────────────────────┬───┘                            │
│     │                     │                                 │
│     │ Simple              │ Complex                         │
│     │                     │                                 │
│  ┌──▼────────────┐   ┌────▼─────────────────┐              │
│  │ Template      │   │ Meta-Prompter        │              │
│  │ Enhancement   │   │                      │              │
│  │               │   │ 1. LLM enhance       │              │
│  │ Fast (1ms)    │   │ 2. Evaluate quality  │              │
│  │ Cheap ($0)    │   │ 3. Recurse (max 2x)  │              │
│  │               │   │                      │              │
│  │ Good for:     │   │ Slow (2-5s)          │              │
│  │ - Simple      │   │ Cost ($0.01-0.05)    │              │
│  │ - Known       │   │                      │              │
│  │   patterns    │   │ Good for:            │              │
│  │               │   │ - Complex requests   │              │
│  │               │   │ - Novel content      │              │
│  │               │   │ - High quality       │              │
│  └───────┬───────┘   └──────┬───────────────┘              │
│          │                  │                               │
│          └──────┬───────────┘                               │
│                 │                                           │
│          Enhanced Prompt                                    │
│                 │                                           │
│                 ▼                                           │
│         Content Generator                                  │
└─────────────────────────────────────────────────────────────┘

Quality Gate Logic:
  if (prompt_complexity < THRESHOLD):
      use template enhancement  # Fast path
  else:
      use meta-prompting        # Quality path
```

---

## Data Flow Comparison

### Current: Tightly Coupled

```
HTTP Request
    │
    ▼
┌─────────────────────────┐
│ main.py                 │
│ • Parse JSON            │───┐
│ • Validate             │   │
│ • Classify domain      │◄──┤ domain_classifier.py
│ • Enhance prompt       │◄──┤ template_engine.py
│ • Call API             │◄──┤ gemini_client.py
│ • Format response      │   │
│ • Handle errors        │   │
└─────────────────────────┘   │
    │                         │
    ▼                         │
HTTP Response                 │
                              │
❌ Can't reuse logic          │
❌ Hard to test               │
❌ HTTP tightly coupled       │
```

### Refactored: Layered

```
HTTP Request
    │
    ▼
┌─────────────────────────┐
│ Flask Route (main.py)   │
│ • Parse JSON            │
│ • Validate              │
│ • Call service          │
│ • Format response       │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ ImageGenerationService  │  ◄─── ✅ Framework-agnostic
│ • classify()            │       ✅ Reusable
│ • enhance()             │       ✅ Testable
│ • generate()            │
└────┬────────────────────┘
     │
     ├──► DomainClassifier (loads YAML)
     │
     ├──► TemplateEngine (loads JSON)
     │
     └──► GeminiClient (async + retry + circuit breaker)

HTTP Response
```

---

## Configuration Evolution

### Current: Hard-Coded

```python
# domain_classifier.py
DOMAIN_KEYWORDS = {
    "photography": ["photo", "portrait", ...],
    "diagrams": ["chart", "flow", ...],
    # 50 lines of keywords
}
```

**Problem**: Adding "presentations" requires code change

---

### Refactored: External YAML

```yaml
# config/domains.yaml
domains:
  photography:
    keywords: [photo, portrait, headshot, ...]
    confidence_threshold: 0.5

  diagrams:
    keywords: [diagram, chart, flowchart, ...]
    confidence_threshold: 0.6

  presentations:  # NEW - no code change!
    keywords: [slide, deck, powerpoint, ...]
    confidence_threshold: 0.5
```

```python
# domain_classifier.py
def __init__(self, config_path="config/domains.yaml"):
    with open(config_path) as f:
        self.domains = yaml.safe_load(f)["domains"]
```

**Benefit**: Add domains by editing YAML, not deploying code

---

### Future: Dynamic Loading

```python
# Auto-discover content types from plugins
for plugin in discover_plugins("content_generators/"):
    register_content_type(plugin)

# API automatically supports new types
GET /content-types
{
  "available": [
    "images",
    "presentations",
    "ui-components",
    "diagrams",
    "videos"
  ]
}
```

---

## Error Handling Evolution

### Current: Scattered

```python
# Every route has this:
try:
    # ... logic ...
except ValueError as e:
    return jsonify({"error": str(e)}), 400
except Exception as e:
    print(f"ERROR: {e}")  # ❌ Print!
    return jsonify({"error": "Internal error"}), 500
```

**Problems**:
- ❌ Duplicated 4 times
- ❌ Print instead of logging
- ❌ No structured error info

---

### Refactored: Centralized

```python
# api/error_handler.py
@handle_api_errors  # Single decorator!
def any_route():
    # Clean logic, no try/except
    if invalid:
        raise ValidationError("Bad input")

    result = service.generate(...)
    return jsonify(result)

# Decorator handles:
# ✅ Logging (structured JSON)
# ✅ Error classification
# ✅ Status codes
# ✅ User-friendly messages
```

**Benefits**:
- ✅ DRY (Don't Repeat Yourself)
- ✅ Consistent error responses
- ✅ Structured logging
- ✅ Easy to add new error types

---

### Future: Circuit Breaker Pattern

```python
# Prevents cascade failures

┌────────────┐
│   Client   │
└─────┬──────┘
      │
      ▼
┌─────────────────┐     ┌──────────────┐
│ Circuit Breaker │────►│ Gemini API   │
│                 │     └──────────────┘
│ States:         │
│ • CLOSED  ✅    │  Requests flow normally
│ • OPEN    🔴    │  Fast-fail (no API calls)
│ • HALF-OPEN 🟡  │  Testing if recovered
└─────────────────┘

If 5 consecutive failures:
  CLOSED → OPEN (stop calling API for 60s)

After 60s:
  OPEN → HALF-OPEN (try 1 request)

If success:
  HALF-OPEN → CLOSED (resume)

If failure:
  HALF-OPEN → OPEN (wait another 60s)
```

---

## Testing Strategy

### Current: Manual Only

```
┌──────────────┐
│ Start Flask  │
│ manually     │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ Send curl        │
│ requests         │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Inspect response │
│ manually         │
└──────────────────┘

❌ Slow
❌ Error-prone
❌ No automation
```

---

### Refactored: Automated Tests

```
┌────────────────────────────────────┐
│ pytest tests/test_critical_paths.py│
└────────┬───────────────────────────┘
         │
         ▼
┌────────────────────────────────────┐
│ Integration Tests                  │
│                                    │
│ 1. test_classify_accuracy()        │
│    ✅ 6 test cases                 │
│                                    │
│ 2. test_template_enhancement()     │
│    ✅ Basic/detailed/expert        │
│                                    │
│ 3. test_gemini_retry_logic()       │
│    ✅ Mocked failures → success    │
│                                    │
│ 4. test_happy_path()               │
│    ✅ End-to-end flow              │
│                                    │
│ 5. test_error_handling()           │
│    ✅ Missing API key, bad model   │
│                                    │
└────────┬───────────────────────────┘
         │
         ▼
┌────────────────────┐
│ Coverage Report    │
│ 82% (target: 80%)  │
└────────────────────┘

✅ Fast (5 seconds)
✅ Automated
✅ CI/CD ready
```

---

## Deployment Comparison

### Current: Hope-Based

```
┌──────────────┐
│ Edit code    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Manual test  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Deploy       │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Hope nothing │
│ breaks 🤞     │
└──────────────┘

Confidence: 60%
```

---

### Refactored: Test-Driven

```
┌──────────────┐
│ Edit code    │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ pytest (5 tests) │
│ ✅ All pass      │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Deploy           │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Structured logs  │
│ monitor health   │
└──────────────────┘

Confidence: 95%
```

---

## Summary: Evolution Path

### Week 1 (Foundation)
```
Monolith
  │
  ├─► Add error handler decorator
  ├─► Add structured logging
  ├─► Extract settings to config
  └─► Write 5 integration tests

Result: Deployable, debuggable
```

### Week 2 (Refactor)
```
Foundation
  │
  ├─► Extract service layer
  ├─► Add classifier interface
  └─► External domain configs

Result: Testable, extensible
```

### Week 5 (Extend)
```
Refactored
  │
  ├─► Add presentation generator
  ├─► Add UI component generator
  ├─► Add diagram generator
  └─► Add video generator

Result: Multi-media factory
```

### Week 9 (Optimize)
```
Extended
  │
  ├─► Integrate meta-prompting
  ├─► Add quality gates
  ├─► LLM-based classification
  └─► A/B testing framework

Result: Intelligent, self-improving
```

---

## Key Metrics

| Metric | Current | After Refactor | After Extension |
|--------|---------|----------------|-----------------|
| **Lines of Code** | 800 | 1,200 | 2,500 |
| **Test Coverage** | 0% | 80% | 85% |
| **Time to Add Feature** | 2 days | 4 hours | 2 hours |
| **Bug Rate** | Unknown | Low (caught by tests) | Very Low |
| **Deployment Confidence** | 60% | 95% | 98% |
| **Content Types** | 1 (images) | 1 (images) | 5 (images, presentations, UI, diagrams, videos) |

---

**Visual Summary**: From monolith → service layer → multi-media factory

*Architecture diagrams are ASCII for easy reference in terminal/docs*
