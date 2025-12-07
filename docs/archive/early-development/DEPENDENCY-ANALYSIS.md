# NanoBanana Project - Complete Dependency Analysis

**Date**: 2025-12-07
**Purpose**: Map all dependencies and analyze atomic nature of each feature for parallel testing

---

## Dependency Tree Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    USER REQUEST                              │
│  "Generate headshot of a CEO"                                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: Prompt Enhancement (generating-image-prompts)     │
│  Dependencies: NONE (can run standalone)                    │
│  Atomic: YES ✅                                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  LAYER 2: Model Selection (nano-banana)                     │
│  Dependencies: Enhanced prompt from Layer 1                 │
│  Atomic: PARTIAL ⚠️ (needs prompt but not API)              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  LAYER 3: Cache Check (nano-banana)                         │
│  Dependencies: Enhanced prompt, Redis                       │
│  Atomic: YES ✅ (Redis can be mocked)                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ├─ Cache HIT → Return cached image ✅
                       │
                       └─ Cache MISS ↓
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────┐
│  LAYER 4: Budget Check (nano-banana)                        │
│  Dependencies: Redis, user_id, cost calculation             │
│  Atomic: YES ✅ (can test with mock Redis)                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ├─ Budget EXCEEDED → Return error ❌
                       │
                       └─ Budget OK ↓
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────┐
│  LAYER 5: API Call (nano-banana)                            │
│  Dependencies: GOOGLE_API_KEY, network, API availability    │
│  Atomic: YES ✅ (standalone API client)                      │
│  CRITICAL: This is where we verify API actually exists! ⚠️   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ├─ API SUCCESS ↓
                       │              │
                       │              ▼
                       │    ┌──────────────────────────────┐
                       │    │ LAYER 6: Cache Store         │
                       │    │ Dependencies: Redis, GCS     │
                       │    │ Atomic: YES ✅                │
                       │    └──────────────────────────────┘
                       │
                       └─ API FAILURE ↓
                                      │
                                      ▼
                       ┌──────────────────────────────────────┐
                       │ LAYER 7: Fallback Strategy          │
                       │ Dependencies: Cache similarity search│
                       │ Atomic: YES ✅                        │
                       └──────────────────────────────────────┘
```

---

## Atomic Feature Breakdown

### Feature 1: Domain Classification ✅ FULLY ATOMIC
**File**: `generating-image-prompts/domain_classifier.py` (NOT YET CREATED)
**Purpose**: Classify user input into Photography/Diagrams/Art/Products

**Dependencies**:
- ✅ NONE (pure function, no external dependencies)

**Inputs**:
- `user_input: str` - Raw user prompt

**Outputs**:
- `domain: str` - One of ["photography", "diagrams", "art", "products"]
- `confidence: float` - Classification confidence (0.0-1.0)

**Testing Strategy**:
```python
# Can test completely independently
def test_domain_classification():
    classifier = DomainClassifier()

    # Test 1: Photography
    assert classifier.classify("headshot of CEO") == "photography"

    # Test 2: Diagrams
    assert classifier.classify("microservices architecture") == "diagrams"

    # Test 3: Art
    assert classifier.classify("impressionist painting") == "art"

    # Test 4: Products
    assert classifier.classify("product photography for e-commerce") == "products"
```

**Atomicity Score**: 10/10 ✅

---

### Feature 2: Template Enhancement ✅ FULLY ATOMIC
**File**: `generating-image-prompts/template_engine.py` (NOT YET CREATED)
**Purpose**: Enhance prompts with domain-specific templates

**Dependencies**:
- ✅ Domain classification (from Feature 1)
- ✅ Template JSON files (static data)

**Inputs**:
- `user_input: str` - Raw prompt
- `domain: str` - Classification from Feature 1
- `quality_tier: str` - One of ["basic", "detailed", "expert"]

**Outputs**:
- `enhanced_prompt: str` - Fully enhanced prompt with technical specs
- `token_count: int` - Number of tokens in enhanced prompt

**Testing Strategy**:
```python
# Can test with mock domain classifier
def test_template_enhancement():
    engine = TemplateEngine()

    enhanced = engine.enhance(
        user_input="CEO headshot",
        domain="photography",
        subcategory="portrait",
        quality_tier="expert"
    )

    # Should include camera specs
    assert "Canon EOS" in enhanced or "Sony A7" in enhanced
    assert "f/1.4" in enhanced or "85mm" in enhanced
    assert len(enhanced) > len("CEO headshot")
```

**Atomicity Score**: 9/10 ✅ (depends on Feature 1 but can mock)

---

### Feature 3: Token Optimization ✅ FULLY ATOMIC
**File**: `generating-image-prompts/token_optimizer.py` (NOT YET CREATED)
**Purpose**: Optimize enhanced prompts to fit token budget

**Dependencies**:
- ✅ NONE (pure function)

**Inputs**:
- `enhanced_prompt: str` - Output from Feature 2
- `token_budget: int` - Maximum tokens (default 500)

**Outputs**:
- `optimized_prompt: str` - Prompt within budget
- `removed_signals: list` - What was removed (for logging)

**Testing Strategy**:
```python
# Completely independent
def test_token_optimization():
    optimizer = TokenOptimizer()

    long_prompt = "..." # 800 token prompt
    optimized = optimizer.optimize(long_prompt, budget=500)

    assert count_tokens(optimized) <= 500
    assert optimized in long_prompt  # Subset, not addition
```

**Atomicity Score**: 10/10 ✅

---

### Feature 4: User Memory System ⚠️ PARTIALLY ATOMIC
**File**: `generating-image-prompts/memory.py` (NOT YET CREATED)
**Purpose**: Store and retrieve user preferences

**Dependencies**:
- ⚠️ SQLite database (external resource)
- ⚠️ File system (for .db file)

**Inputs**:
- `user_id: str`
- `preferences: dict` - User preferences to store

**Outputs**:
- `preferences: dict` - Retrieved preferences

**Testing Strategy**:
```python
# Can test with in-memory SQLite
def test_user_memory():
    memory = UserMemory(db_path=":memory:")  # In-memory DB

    # Store preferences
    memory.save_preferences("user123", {
        "default_model": "flash",
        "favorite_style": "portrait"
    })

    # Retrieve preferences
    prefs = memory.get_preferences("user123")
    assert prefs["default_model"] == "flash"
```

**Atomicity Score**: 7/10 ⚠️ (requires database, but can mock)

---

### Feature 5: Prompt Complexity Analyzer ✅ FULLY ATOMIC
**File**: `nano-banana/complexity_analyzer.py` (NOT YET CREATED)
**Purpose**: Analyze prompt complexity for model selection

**Dependencies**:
- ✅ NONE (pure function)

**Inputs**:
- `prompt: str` - Enhanced prompt

**Outputs**:
- `complexity_score: float` - 0.0 (simple) to 1.0 (complex)
- `factors: dict` - Breakdown (token_count, tech_specs, etc.)

**Testing Strategy**:
```python
# Completely independent
def test_complexity_analysis():
    analyzer = ComplexityAnalyzer()

    # Simple prompt
    simple = "a red ball"
    assert analyzer.analyze(simple) < 0.3

    # Complex prompt
    complex = "professional portrait shot on Canon EOS R5..."
    assert analyzer.analyze(complex) > 0.7
```

**Atomicity Score**: 10/10 ✅

---

### Feature 6: Model Selection ✅ FULLY ATOMIC
**File**: `nano-banana/model_selector.py` (NOT YET CREATED)
**Purpose**: Select Flash vs Pro based on complexity and budget

**Dependencies**:
- ✅ Complexity score (from Feature 5)
- ✅ User preferences (can be mocked)

**Inputs**:
- `complexity_score: float`
- `user_budget_remaining: float`
- `quality_tier: str`

**Outputs**:
- `model: str` - "flash" or "pro"
- `reasoning: str` - Why this model was selected

**Testing Strategy**:
```python
# Can test with mock data
def test_model_selection():
    selector = ModelSelector()

    # Low budget → Flash
    model = selector.select(
        complexity=0.8,
        budget_remaining=0.05,  # Can't afford Pro
        quality_tier="expert"
    )
    assert model == "flash"

    # High complexity + budget → Pro
    model = selector.select(
        complexity=0.9,
        budget_remaining=10.0,
        quality_tier="expert"
    )
    assert model == "pro"
```

**Atomicity Score**: 10/10 ✅

---

### Feature 7: Cache Key Generation ✅ FULLY ATOMIC
**File**: `nano-banana/cache.py` (NOT YET CREATED)
**Purpose**: Generate deterministic cache keys

**Dependencies**:
- ✅ NONE (pure function using hashlib)

**Inputs**:
- `prompt: str`
- `model: str`
- `params: dict`

**Outputs**:
- `cache_key: str` - "nanobanana:v1:{hash}"

**Testing Strategy**:
```python
# Completely deterministic
def test_cache_key_generation():
    cache = CacheManager()

    key1 = cache.generate_key("test prompt", "flash", {})
    key2 = cache.generate_key("test prompt", "flash", {})

    # Same inputs → same key
    assert key1 == key2

    # Different inputs → different key
    key3 = cache.generate_key("test prompt", "pro", {})
    assert key1 != key3
```

**Atomicity Score**: 10/10 ✅

---

### Feature 8: Cache Operations ⚠️ PARTIALLY ATOMIC
**File**: `nano-banana/cache.py` (NOT YET CREATED)
**Purpose**: L1 → L2 → L3 cache checking and storing

**Dependencies**:
- ⚠️ Redis (external service)
- ⚠️ GCS (external service)

**Inputs**:
- `cache_key: str`
- `image_data: bytes` (for storing)

**Outputs**:
- `cached_image: dict | None`

**Testing Strategy**:
```python
# Can test with mock Redis/GCS
def test_cache_operations():
    # Mock Redis
    redis_mock = fakeredis.FakeRedis()
    gcs_mock = MockGCSClient()

    cache = CacheManager(redis=redis_mock, gcs=gcs_mock)

    # Store
    cache.store("key123", image_data)

    # Retrieve
    cached = cache.get("key123")
    assert cached is not None
```

**Atomicity Score**: 6/10 ⚠️ (requires external services, but can mock)

---

### Feature 9: Cost Tracking (Atomic) ✅ FULLY ATOMIC (WITH REDIS)
**File**: `nano-banana/cost_tracker.py` (NOT YET CREATED)
**Purpose**: Atomic budget check and increment

**Dependencies**:
- ⚠️ Redis (for Lua script execution)

**Inputs**:
- `user_id: str`
- `cost_usd: float`
- `daily_limit_usd: float`

**Outputs**:
- `allowed: bool` - Whether cost is within budget
- `current_spend: float` - Current spend

**Testing Strategy**:
```python
# Can test with fake Redis
def test_atomic_cost_tracking():
    redis_mock = fakeredis.FakeRedis()
    tracker = CostTracker(redis=redis_mock)

    # First call - should succeed
    allowed, spend = tracker.check_and_increment(
        "user123", cost=0.039, limit=10.0
    )
    assert allowed is True
    assert spend == 0.039

    # Exceed budget
    allowed, spend = tracker.check_and_increment(
        "user123", cost=10.0, limit=10.0
    )
    assert allowed is False  # Would exceed
```

**Atomicity Score**: 8/10 ✅ (atomic with Redis, can mock for testing)

---

### Feature 10: API Client ❌ NOT ATOMIC (CRITICAL DEPENDENCY)
**File**: `nano-banana/api_client.py` (EXISTS BUT NEEDS TESTING)
**Purpose**: Call Google NanoBanana/Gemini API

**Dependencies**:
- ❌ **GOOGLE_API_KEY** (environment variable)
- ❌ **Network connectivity**
- ❌ **API endpoint availability** (UNVERIFIED!)

**Inputs**:
- `prompt: str`
- `model: str` - "flash" or "pro"
- `aspect_ratio: str`

**Outputs**:
- `image_url: str`
- `metadata: dict`

**Testing Strategy**:
```python
# REQUIRES REAL API KEY
def test_api_client_real():
    client = NanoBananaClient(api_key=os.getenv("GOOGLE_API_KEY"))

    # Test 1: Verify API endpoint exists
    result = client.generate_image(
        prompt="a simple test image",
        model="flash"
    )

    # This will fail if API doesn't exist!
    assert result["image_url"] is not None
```

**Atomicity Score**: 2/10 ❌ (CRITICAL: Cannot test without real API, and API may not exist!)

---

### Feature 11: Circuit Breaker ⚠️ PARTIALLY ATOMIC
**File**: `nano-banana/circuit_breaker.py` (EXISTS BUT NEEDS FIX)
**Purpose**: Prevent cascading failures

**Dependencies**:
- ⚠️ **Redis** (if distributed - currently NOT distributed!)
- ⚠️ Time-based state (uses time.time())

**Inputs**:
- `service_name: str`
- `function: Callable` - Function to protect

**Outputs**:
- `result: Any` - Function result or exception

**Testing Strategy**:
```python
# Can test with mock failures
def test_circuit_breaker():
    cb = CircuitBreaker(failure_threshold=3)

    # Simulate failures
    for i in range(3):
        try:
            cb.call(lambda: raise_error())
        except:
            pass

    # Should be OPEN now
    assert cb.state == CircuitState.OPEN

    # Next call should fail fast
    with pytest.raises(CircuitBreakerOpenError):
        cb.call(lambda: "success")
```

**Atomicity Score**: 7/10 ⚠️ (Works standalone, but NOT distributed - bug!)

---

### Feature 12: Exponential Backoff ✅ FULLY ATOMIC
**File**: `nano-banana/retry.py` (NOT YET CREATED)
**Purpose**: Retry with exponential backoff + jitter

**Dependencies**:
- ✅ NONE (pure logic)

**Inputs**:
- `func: Callable`
- `max_retries: int`

**Outputs**:
- `result: Any` - Function result or exception

**Testing Strategy**:
```python
# Completely testable
def test_exponential_backoff():
    call_count = 0

    def flaky_function():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise APITimeoutError()
        return "success"

    result = call_with_retry(flaky_function, max_retries=3)

    assert call_count == 3
    assert result == "success"
```

**Atomicity Score**: 10/10 ✅

---

## Dependency Matrix

| Feature | External Deps | Can Mock? | Standalone Test? | Score |
|---------|---------------|-----------|------------------|-------|
| Domain Classification | None | N/A | ✅ YES | 10/10 |
| Template Enhancement | Templates | ✅ YES | ✅ YES | 9/10 |
| Token Optimization | None | N/A | ✅ YES | 10/10 |
| User Memory | SQLite | ✅ YES | ✅ YES | 7/10 |
| Complexity Analyzer | None | N/A | ✅ YES | 10/10 |
| Model Selector | None | N/A | ✅ YES | 10/10 |
| Cache Key Gen | None | N/A | ✅ YES | 10/10 |
| Cache Ops | Redis, GCS | ✅ YES | ⚠️ PARTIAL | 6/10 |
| Cost Tracker | Redis | ✅ YES | ✅ YES | 8/10 |
| **API Client** | **API Key, Network** | ❌ **NO** | ❌ **NO** | **2/10** |
| Circuit Breaker | Redis (should) | ⚠️ PARTIAL | ⚠️ PARTIAL | 7/10 |
| Exponential Backoff | None | N/A | ✅ YES | 10/10 |

**Average Atomicity**: 8.25/10 (without API client: 9.1/10)

---

## Critical Findings

### 🔴 BLOCKER: API Client Cannot Be Tested Atomically

The **API Client (Feature 10)** is the **ONLY** component that:
1. **Cannot be mocked** (need real API response format)
2. **Requires network** (cannot test offline)
3. **Requires valid API key** (now provided)
4. **May not exist** (MERCURIO/MARS claim NanoBanana API doesn't exist)

**This is the critical test that will determine if the entire project is viable.**

---

## Testing Strategy

### Phase 1: Atomic Feature Tests (Parallel) ✅ CAN TEST NOW
Test all features 1-9, 11-12 in parallel **without API client**:

1. Domain Classification
2. Template Enhancement
3. Token Optimization
4. User Memory
5. Complexity Analyzer
6. Model Selector
7. Cache Key Generation
8. Cache Operations (with mock Redis/GCS)
9. Cost Tracker (with mock Redis)
10. ~~API Client~~ (SKIP for now)
11. Circuit Breaker (with mock Redis)
12. Exponential Backoff

**Can use parallel test agents for features 1-9, 11-12** ✅

---

### Phase 2: API Client Test (Sequential) ❌ CRITICAL BLOCKER

**Must answer these questions BEFORE implementing anything else**:

1. ✅ Do we have a valid API key? → **YES** (provided: <GOOGLE_API_KEY_REDACTED>)
2. ❌ Does the NanoBanana API endpoint exist?
3. ❌ What is the correct endpoint URL?
4. ❌ What are the correct model names ("flash", "pro")?
5. ❌ What is the request/response format?
6. ❌ What is the actual pricing?

**Test Plan**:
```python
import httpx
import os

async def test_nanobanana_api_exists():
    """
    CRITICAL TEST: Verify NanoBanana API actually exists

    This test will determine if we need to:
    A) Continue with NanoBanana implementation
    B) Switch to Vertex AI Imagen
    C) Rethink entire approach
    """

    api_key = os.getenv("GOOGLE_API_KEY")

    # Try possible endpoints
    endpoints = [
        "https://api.nanobanana.google.com/v1/images/generate",
        "https://generativelanguage.googleapis.com/v1/images/generate",
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateImage",
        "https://aiplatform.googleapis.com/v1/projects/{project}/locations/us-central1/publishers/google/models/imagegeneration:predict"
    ]

    for endpoint in endpoints:
        try:
            response = await httpx.post(
                endpoint,
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "prompt": "a red ball",
                    "model": "flash"
                },
                timeout=30.0
            )

            print(f"✅ Endpoint {endpoint} responded: {response.status_code}")
            print(f"Response: {response.text}")

            if response.status_code in [200, 201]:
                return endpoint  # FOUND IT!

        except Exception as e:
            print(f"❌ Endpoint {endpoint} failed: {e}")

    raise ValueError("NO VALID NANOBANANA API ENDPOINT FOUND!")
```

---

## Dependency Graph (Visual)

```
User Input
    │
    ├─→ Domain Classification (atomic) ✅
    │       │
    │       └─→ Template Enhancement (atomic) ✅
    │               │
    │               └─→ Token Optimization (atomic) ✅
    │                       │
    │                       └─→ Enhanced Prompt
    │
    └─→ User Memory (atomic with mock DB) ✅
            │
            └─→ User Preferences


Enhanced Prompt + User Preferences
    │
    └─→ Complexity Analyzer (atomic) ✅
            │
            └─→ Model Selector (atomic) ✅
                    │
                    └─→ Selected Model ("flash" or "pro")


Selected Model + Enhanced Prompt
    │
    ├─→ Cache Key Generator (atomic) ✅
    │       │
    │       └─→ Cache Lookup (needs Redis mock) ⚠️
    │               │
    │               ├─ HIT → Return cached image ✅
    │               │
    │               └─ MISS ↓
    │
    └─→ Cost Tracker (needs Redis mock) ⚠️
            │
            ├─ EXCEEDED → Error ❌
            │
            └─ OK ↓
                │
                └─→ API Client (needs REAL API) ❌ BLOCKER
                        │
                        ├─→ Circuit Breaker (needs Redis for distributed) ⚠️
                        │
                        └─→ Exponential Backoff (atomic) ✅
                                │
                                ├─ SUCCESS → Store in Cache ✅
                                │
                                └─ FAILURE → Fallback Strategy ✅
```

---

## Parallel Testing Plan

### Batch 1: Pure Functions (No External Deps) - 5 agents
1. **Agent 1**: Domain Classification
2. **Agent 2**: Token Optimization
3. **Agent 3**: Complexity Analyzer
4. **Agent 4**: Model Selector
5. **Agent 5**: Cache Key Generator

**Can start immediately** ✅

---

### Batch 2: Functions with Mockable Deps - 4 agents
6. **Agent 6**: Template Enhancement (needs templates)
7. **Agent 7**: User Memory (needs SQLite mock)
8. **Agent 8**: Exponential Backoff (needs mock failures)
9. **Agent 9**: Fallback Strategy (needs mock cache)

**Can start after templates created** ✅

---

### Batch 3: Redis-Dependent - 2 agents
10. **Agent 10**: Cache Operations (needs fakeredis)
11. **Agent 11**: Cost Tracker (needs fakeredis)

**Can start with fakeredis library** ✅

---

### Batch 4: Critical API Test - 1 agent
12. **Agent 12**: API Client (needs REAL Google API key)

**BLOCKS entire project** ❌

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| NanoBanana API doesn't exist | **90%** | **CRITICAL** | Test with real API key FIRST |
| API exists but different format | 70% | HIGH | Document actual format |
| API exists but different pricing | 50% | MEDIUM | Update cost calculations |
| Redis not available locally | 20% | LOW | Use fakeredis for tests |
| GCS not configured | 30% | LOW | Mock GCS for tests |
| SQLite permissions | 10% | LOW | Use :memory: for tests |

---

## Recommended Testing Order

1. **FIRST**: Test API Client with real API key (Agent 12) ← **DO THIS NOW**
2. **THEN**: If API exists → Parallel test all atomic features (Agents 1-11)
3. **FINALLY**: Integration test with real API

**Rationale**: No point testing 11 features if the 12th (API) doesn't exist!

---

## Next Steps

1. ✅ Create test environment with API key (DONE)
2. ❌ Test API client to verify endpoint exists (**CRITICAL - DO NEXT**)
3. ⏳ Based on API test results:
   - If API exists → Implement and test all features
   - If API doesn't exist → Switch to Vertex AI Imagen
   - If neither works → Rethink approach per MARS recommendation

---

**Status**: Ready for parallel testing of Features 1-9, 11-12
**Blocker**: Feature 10 (API Client) must be tested with real API key before proceeding
