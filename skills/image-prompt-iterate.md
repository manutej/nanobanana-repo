# SKILL: Image Prompt Iterate

## Purpose
Recursively improve AI image generation prompts through quality-driven iteration with automatic visual assessment and prompt refinement.

## Description
Meta-prompting workflow adapted for image generation:
1. **Analyze** visual complexity (scene composition, detail level, concept abstraction)
2. **Generate** initial image with base prompt
3. **Assess** visual quality (clarity, concept accuracy, text rendering, composition)
4. **Extract** successful patterns (colors, layouts, styles that worked)
5. **Refine** prompt based on gaps (missing elements, unclear text, composition issues)
6. **Iterate** until quality threshold met or max iterations reached

## When to Use

**Use for:**
- Technical diagrams requiring precise text and labels
- Abstract concepts needing clear visual metaphors
- Production-ready images for presentations/publications
- Complex multi-element compositions
- Images where first attempt had issues (misspellings, missing elements)

**Don't use for:**
- Simple one-off images (direct generation is faster)
- Exploratory ideation (just generate variations)
- Time-critical needs (iteration adds latency)

## Visual Quality Assessment Criteria

| Criterion | Weight | What to Check |
|-----------|--------|---------------|
| **Text Rendering** | 30% | Spelling accuracy, readability, correct labels |
| **Concept Accuracy** | 25% | Visual matches intended concept/metaphor |
| **Composition** | 20% | Balance, hierarchy, visual flow |
| **Clarity** | 15% | Clean lines, distinct elements, professional aesthetic |
| **Completeness** | 10% | All requested elements present |

**Scoring**: 0.0-1.0 scale
- 0.90+: Production-ready
- 0.75-0.89: Good, minor refinements
- 0.60-0.74: Acceptable, needs iteration
- <0.60: Significant issues, refine prompt

## Iteration Strategy

### Iteration 1: Baseline Generation
Generate with detailed, explicit prompt:
- Exact text to render (with spelling)
- Color specifications (hex codes if critical)
- Layout/composition instructions
- Style guidelines

### Iteration 2: Gap-Filling Refinement
If quality < threshold:
- Identify specific gaps (missing icons, wrong colors, text errors)
- Add explicit corrections to prompt
- Emphasize previously weak areas

### Iteration 3: Final Polish
If still needed:
- Fine-tune remaining issues
- Add photographic language ("high contrast", "clean white background")
- Specify exact positioning for problem elements

## Prompt Enhancement Patterns

### For Technical Diagrams
```
Original: "Diagram showing API architecture"

Enhanced: "Horizontal architecture diagram with 3 tiers:
TOP: Blue rounded box labeled 'Client Layer' (sans-serif, bold)
MIDDLE: Green boxes (3) labeled 'API Gateway', 'Auth Service', 'Rate Limiter'
BOTTOM: Orange cylinders (2) labeled 'Database' and 'Cache'
Arrows connecting tiers. White background, clean modern style."
```

### For Abstract Concepts
```
Original: "Visualize neural network learning"

Enhanced: "Abstract visualization of neural network training:
LEFT: Network with random weights (gray tangled connections)
CENTER: Gradient descent process (downward arrows, loss curve)
RIGHT: Optimized network (organized blue connections, clear patterns)
Bottom: Graph showing decreasing loss over epochs
Mathematical formula: θ = θ - α∇J(θ)
Scientific illustration style, white background"
```

### For Text-Heavy Images
```
Original: "Dashboard with metrics"

Enhanced: "Dashboard layout with 6 metric cards:
Card 1: 'Latency' | Before: 3.2s (red) | After: 0.9s (green) | ↓ 72%
Card 2: 'Cost' | Before: $0.50 (red) | After: $0.12 (green) | ↓ 76%
[Specify exact text for ALL cards]
Clean card borders, consistent typography, white background"
```

## Usage Examples

### Example 1: Technical Diagram Iteration

**Task**: Generate 7-layer context engineering stack

**Iteration 1** (Quality: 0.75):
```
Issues identified:
- Layer 4 text misspelled ("Converstion" instead of "Conversation")
- Icons not distinct enough
- Missing data flow arrow
```

**Iteration 2 Prompt Enhancement**:
```
ADDED:
- Explicit spelling: "Layer 4: CONVERSATION MEMORY (spelled C-O-N-V-E-R-S-A-T-I-O-N)"
- Icon specifications: "Layer 4: Chat bubble icon (distinct from Layer 1 question mark)"
- Missing element: "RIGHT SIDE: Vertical upward arrow labeled 'Context Assembly Flow'"
```

**Result** (Quality: 0.94): Production-ready diagram with perfect text

### Example 2: Abstract Concept Iteration

**Task**: Visualize "Intelligence Through Crossing" (genetic recombination)

**Iteration 1** (Quality: 0.68):
```
Issues:
- Crossover event not clear
- Offspring traits hard to distinguish
- Missing performance metrics
```

**Iteration 2 Enhancement**:
```
ADDED:
- "CENTER: Large X-shaped crossing point (red highlight) showing chromosome exchange"
- "Offspring: Blue-green hybrid colors (clearly different from parent colors)"
- "RIGHT: Bar graph showing Parent 1: 70%, Parent 2: 75%, Offspring 1: 85% (emergence highlighted)"
```

**Result** (Quality: 0.92): Clear visual showing recombination emergence

## Configuration

### Recommended Settings by Use Case

**Production Diagrams** (client-facing):
```
max_iterations: 3
quality_threshold: 0.90
model: "pro"  # Gemini 3 Pro for best text rendering
save_intermediates: true
```

**Prototyping/Exploration**:
```
max_iterations: 2
quality_threshold: 0.75
model: "flash"  # Faster, cheaper
save_intermediates: false
```

**Complex Abstract Concepts**:
```
max_iterations: 4
quality_threshold: 0.85
model: "pro"
assess_visual_metaphor: true
```

## Output Structure

```
.prompts/image-iterations/
  001-context-stack-initial/
    prompt.md           # Original detailed prompt
    image.png           # Generated image
    assessment.json     # Quality score + issues identified
    refinements.md      # Planned improvements for iteration 2
  002-context-stack-refined/
    prompt.md           # Enhanced prompt with fixes
    image.png           # Improved image
    assessment.json     # New quality score
  FINAL.png             # Best iteration
  metadata.json         # All iteration data
```

## Integration with NanoBanana

### Standalone Usage
```python
from simple_batch import generate_batch_streaming

# Manual iteration
prompts_v1 = ["Initial prompt"]
# Generate, assess, refine
prompts_v2 = ["Enhanced prompt with fixes"]
# Generate again
```

### With Meta-Prompting Engine
```python
# Future: Automated iteration with quality assessment
result = iterate_image_prompt(
    initial_prompt="Diagram showing...",
    max_iterations=3,
    quality_threshold=0.90,
    model="pro"
)
# Returns best image + metadata
```

## Quality Assessment Checklist

After each generation, evaluate:

**Text Rendering** (30 points):
- [ ] All labels spelled correctly (10 pts)
- [ ] Text readable and properly sized (10 pts)
- [ ] Fonts/styles match specification (10 pts)

**Concept Accuracy** (25 points):
- [ ] Visual metaphor clear and accurate (15 pts)
- [ ] All key concept elements present (10 pts)

**Composition** (20 points):
- [ ] Balanced layout (10 pts)
- [ ] Clear visual hierarchy (10 pts)

**Clarity** (15 points):
- [ ] Clean lines and distinct elements (10 pts)
- [ ] Professional aesthetic (5 pts)

**Completeness** (10 points):
- [ ] All requested elements included (10 pts)

**Total Score**: Sum / 100 = Quality (0.0-1.0)

## Best Practices

1. **Be Explicit**: Don't assume - specify exact text, colors, positions
2. **Iterate Strategically**: Focus each iteration on biggest gaps
3. **Use Pro Model for Production**: Text rendering quality worth the 3x cost
4. **Save Intermediates**: Learn what works for future prompts
5. **Assess Honestly**: Don't inflate scores - gaps help refine

## Common Refinement Patterns

**Issue**: Misspelled text
**Fix**: Add explicit spelling in prompt: "labeled 'DATABASE' (D-A-T-A-B-A-S-E)"

**Issue**: Missing visual element
**Fix**: Add to prompt: "TOP RIGHT: Security shield icon (must be present)"

**Issue**: Wrong colors
**Fix**: Use hex codes: "Blue bars (#2196F3), not dark blue or purple"

**Issue**: Cluttered composition
**Fix**: "White background, 60px spacing between elements, clean minimal style"

**Issue**: Abstract concept unclear
**Fix**: Add explicit visual metaphor: "Represent as flowing water (smooth curves) vs rigid blocks (sharp edges)"

## Workflow Summary

```
1. Generate with detailed base prompt (model: flash or pro)
   ↓
2. Assess quality (score 0.0-1.0, identify gaps)
   ↓
3. If quality < threshold:
   - Extract successful patterns
   - Identify gaps
   - Enhance prompt with explicit fixes
   - Generate iteration 2
   ↓
4. Repeat until threshold met or max iterations
   ↓
5. Return best image + metadata
```

## Expected Outcomes

**After 1 iteration**: 70-85% success rate (good but may have minor issues)
**After 2 iterations**: 85-95% success rate (production-quality)
**After 3 iterations**: 95%+ success rate (publication-ready)

**Cost**: Pro model iterations = $0.12 × iterations
**Time**: ~30-60s per iteration (async batch)

## Source
Adapted from `/meta_prompting_engine` for image generation workflows
Compatible with NanoBanana Pro (Gemini 3 Pro Image) pipeline
