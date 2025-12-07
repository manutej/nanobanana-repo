# 🍌 NanoBanana - AI Image Generation Plugin for Claude Code

**Production-ready image generation powered by Gemini Pro**

Generate technical diagrams, abstract visualizations, and professional visual content with state-of-the-art quality and perfect text rendering.

---

## ✨ Features

- **🎯 100% Success Rate** - Validated async batch processing with zero failures
- **💎 Pro Model Quality** - Gemini 3 Pro: Perfect text rendering, 4K resolution
- **⚡ Fast & Efficient** - Async batch processing with smart concurrency control
- **🎨 Dual Quality Tiers** - Flash ($0.039) for prototyping, Pro ($0.12) for production
- **📚 Pre-Built Libraries** - Context Engineering (10 diagrams) + Symbolic Concepts (8 visualizations)
- **🔄 Meta-Prompting** - Iterative prompt refinement for perfect results
- **🛡️ Secure by Default** - API keys in .env only, pre-commit hooks prevent exposure

---

## 🚀 Quick Start

### Option 1: GitHub Clone

```bash
# Clone repository
git clone https://github.com/manutej/nanobanana-repo.git
cd nanobanana-repo

# Setup environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# Test installation
python examples/generate_context_engineering_pro.py
```

### Option 2: Claude Code Plugin

```bash
# In Claude Code
/plugin install nanobanana

# Or manually
mkdir -p ~/.claude/plugins
git clone https://github.com/manutej/nanobanana-repo.git ~/.claude/plugins/nanobanana
cd ~/.claude/plugins/nanobanana
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your GOOGLE_API_KEY to .env
```

---

## 🔑 Getting Your API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **"Get API Key"** or **"Create API Key"**
3. Copy the key (starts with `AIza...`)
4. Add to `.env` file:
   ```bash
   GOOGLE_API_KEY=AIzaSy...your_actual_key_here
   ```

**⚠️ NEVER commit your .env file to Git!** (Already in .gitignore)

---

## 📖 Usage Examples

### 1. Generate Single Image

```python
import asyncio
from src.gemini_client import GeminiClient

async def main():
    async with GeminiClient() as client:
        result = await client.generate_image(
            "Professional technical diagram showing 3-tier web architecture",
            model="pro"  # or "flash" for faster/cheaper
        )

        with open("output.png", "wb") as f:
            f.write(result["image_data"])

        print(f"Generated: {len(result['image_data']) / 1024:.1f} KB")

asyncio.run(main())
```

### 2. Batch Generation (Async Streaming)

```python
from examples.simple_batch import generate_batch_streaming

prompts = [
    "Diagram of RAG pipeline with 5 steps",
    "Flowchart showing decision tree",
    "Bar chart comparing before/after metrics"
]

async for result in generate_batch_streaming(prompts, max_concurrent=5):
    if result["status"] == "success":
        filename = f"image_{result['index']}.png"
        with open(filename, "wb") as f:
            f.write(result["image_data"])
        print(f"✓ {filename} ({result['size_mb']:.2f} MB)")
```

### 3. Pre-Built Examples

**Context Engineering** (10 technical diagrams):
```bash
python examples/generate_context_engineering_pro.py
# Output: examples/Context Engineering Pro/*.png
# Use case: LLM context optimization webinar
```

**Symbolic Concepts** (8 abstract visualizations):
```bash
python examples/generate_symbolic_concepts.py
# Output: examples/Symbolic Concepts/*.png
# Use case: Advanced concepts (Fourier kinesthetics, nanobots, etc.)
```

---

## 🎨 Model Comparison

| Feature | Flash Model | Pro Model |
|---------|------------|-----------|
| **Model ID** | gemini-2.5-flash-image | gemini-3-pro-image-preview |
| **Cost** | $0.039/image | $0.12/image |
| **Speed** | Fast (~5-10s) | Medium (~10-20s) |
| **Text Rendering** | Good (67-80% accuracy) | Excellent (~100% accuracy) ✅ |
| **Resolution** | Standard | Up to 4K |
| **Best For** | Prototyping, exploration | Production, client-facing |

**Recommendation**: Use Flash for testing, Pro for final deliverables

---

## 🧠 Meta-Prompting Skill

Iteratively refine prompts for perfect results:

```markdown
Skill: image-prompt-iterate

Process:
1. Generate with base prompt
2. Assess quality (text, composition, clarity)
3. Extract gaps (misspellings, missing elements)
4. Refine prompt with explicit fixes
5. Regenerate until quality threshold met

Example:
Iteration 1: "Diagram showing API architecture" → Quality: 0.75
Issues: Missing labels, unclear flow

Iteration 2: Enhanced prompt with:
- "Three horizontal tiers labeled 'Client', 'API', 'Database'"
- "Arrows showing data flow left-to-right"
- "Blue boxes for client, green for API, orange for database"
→ Quality: 0.94 ✅ Production-ready
```

See `skills/image-prompt-iterate.md` for complete guide.

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [GEMINI-IMAGEN-MODELS.md](docs/research/GEMINI-IMAGEN-MODELS.md) | Complete model comparison + best practices |
| [ASYNC-BATCH-BREAKTHROUGH.md](docs/ASYNC-BATCH-BREAKTHROUGH.md) | Technical deep-dive on async pattern |
| [CONTEXT-ENGINEERING-RESEARCH.md](docs/research/CONTEXT-ENGINEERING-RESEARCH.md) | LLM context optimization research |
| [COMONADIC-PATTERN-ANALYSIS.md](docs/COMONADIC-PATTERN-ANALYSIS.md) | Pattern extraction for async batch |

---

## 🎯 Use Cases

**Technical Presentations**:
- Architecture diagrams
- Flowcharts and decision trees
- System component diagrams
- Data flow visualizations

**Educational Materials**:
- Concept illustrations
- Process diagrams
- Comparison charts
- Tutorial graphics

**Abstract Concepts**:
- Scientific visualizations
- Mathematical concepts
- Philosophical ideas
- Symbolic representations

**Business/Marketing**:
- Metrics dashboards
- Before/after comparisons
- ROI visualizations
- Process improvements

---

## 🔧 Configuration

### Environment Variables

```bash
# Required
GOOGLE_API_KEY=your_key_here

# Optional
NANOBANANA_DEFAULT_MODEL=flash  # or "pro"
```

### Model Selection in Code

```python
# Flash model (fast, cheap)
result = await client.generate_image(prompt, model="flash")

# Pro model (high quality)
result = await client.generate_image(prompt, model="pro")
```

---

## 🛡️ Security

**API Key Protection**:
- ✅ Keys stored in `.env` only (gitignored)
- ✅ Pre-commit hooks scan for accidental exposure
- ✅ CLAUDE.md contains security rules
- ✅ No keys in code, docs, or examples

**Pre-Commit Hook**:
Automatically installed hooks prevent commits with exposed keys:
```bash
chmod +x .git/hooks/pre-commit
# Scans for AIza, sk-, ghp-, AKIA patterns
# Blocks commit if detected
```

---

## 📊 Validated Performance

**Context Engineering Suite** (10 images):
- Success Rate: 100% (10/10) ✅
- Zero spelling errors
- Average size: 470 KB (43% smaller than Flash)
- Total cost: $1.20

**Symbolic Concepts Suite** (8 images):
- Success Rate: 100% (8/8) ✅
- Perfect concept accuracy
- Average size: 550 KB
- Total cost: $0.96

**Combined**: 18 images, 100% success, $2.16 total

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Ensure no API keys in commits
5. Submit pull request

---

## 📜 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- Built with [Google Gemini API](https://ai.google.dev/)
- Async pattern inspired by comonadic extraction
- Meta-prompting adapted from recursive refinement techniques
- Research powered by Context7 MCP

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/manutej/nanobanana-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/manutej/nanobanana-repo/discussions)
- **Documentation**: See `docs/` directory

---

## 🚀 Roadmap

**Current (v1.0)**:
- ✅ Flash + Pro model support
- ✅ Async batch processing
- ✅ Meta-prompting skill
- ✅ Pre-built example libraries

**Planned (v1.1)**:
- ⏭️ Automated quality scoring
- ⏭️ Multi-format export (PNG, SVG, PDF)
- ⏭️ Prompt template library
- ⏭️ Interactive refinement UI

**Future**:
- ⏭️ Native Batch API integration (for 100+ images)
- ⏭️ Video generation support
- ⏭️ Multi-modal iteration (text + image feedback)

---

**Built with ❤️ for Claude Code users**

Generate production-quality images with ease! 🎨✨
