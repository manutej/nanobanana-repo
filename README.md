# 🍌 NanoBanana

**Production-ready AI image generation powered by Gemini Pro**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Success Rate](https://img.shields.io/badge/success%20rate-100%25-brightgreen.svg)](docs/CONTEXT-ENGINEERING-PIPELINE-TEST.md)

Generate technical diagrams, abstract visualizations, and professional visual content with state-of-the-art quality and perfect text rendering.

---

## ✨ Features

- 🎯 **100% Success Rate** - Validated async batch processing
- 💎 **Pro Model Quality** - Perfect text rendering, 4K resolution
- ⚡ **Fast & Efficient** - Smart concurrency control, zero rate limits
- 🎨 **Dual Quality Tiers** - Flash ($0.039) for prototyping, Pro ($0.12) for production
- 📚 **Pre-Built Libraries** - 18 production-ready example images included
- 🔄 **Meta-Prompting** - Iterative refinement for perfect results
- 🛡️ **Secure by Default** - API keys protected, pre-commit hooks

---

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/manutej/nanobanana-repo.git
cd nanobanana-repo

# Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY from https://aistudio.google.com/app/apikey

# Test with Pro model
python examples/generate_context_engineering_pro.py
```

**Result**: 10 production-quality technical diagrams in `examples/Context Engineering Pro/`

---

## 📖 Usage

### Single Image

```python
import asyncio
from src.gemini_client import GeminiClient

async def main():
    async with GeminiClient() as client:
        result = await client.generate_image(
            "Technical diagram showing 3-tier architecture with labeled components",
            model="pro"  # or "flash" for faster/cheaper
        )

        with open("output.png", "wb") as f:
            f.write(result["image_data"])

asyncio.run(main())
```

### Batch Generation

```python
from examples.simple_batch import generate_batch_streaming

prompts = [
    "Flowchart showing decision tree with 5 steps",
    "Bar chart comparing metrics before and after optimization",
    "System architecture diagram with client, API, and database tiers"
]

async for result in generate_batch_streaming(prompts, max_concurrent=5):
    if result["status"] == "success":
        print(f"✓ Generated {result['size_mb']:.2f} MB image")
```

### Flask API (service mode)

`src/main.py` now supports:
- `POST /generate` with optional `aspect_ratio`, `image_size`, and `brand_profile`
- `POST /generate/batch` with bounded `max_concurrent` and per-item status
- `GET /brand-profiles` to inspect available brand constraints

---

## 🎨 Model Comparison

| Feature | Flash | Pro |
|---------|-------|-----|
| **Cost** | $0.039 | $0.12 |
| **Speed** | Fast (5-10s) | Medium (10-20s) |
| **Text Accuracy** | 70-80% | **~100%** ✅ |
| **Best For** | Prototyping | Production |

**Get API Key**: [Google AI Studio](https://aistudio.google.com/app/apikey) (free tier available)

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[PLUGIN-README.md](PLUGIN-README.md)** | Complete plugin guide (installation, examples, API) |
| **[GEMINI-IMAGEN-MODELS.md](docs/research/GEMINI-IMAGEN-MODELS.md)** | Model comparison & best practices |
| **[ASYNC-BATCH-BREAKTHROUGH.md](docs/ASYNC-BATCH-BREAKTHROUGH.md)** | Technical deep-dive on async pattern |
| **[image-prompt-iterate.md](skills/image-prompt-iterate.md)** | Meta-prompting for iterative refinement |

---

## 🎯 Examples Included

**Context Engineering** (10 diagrams - $1.20):
- 7-Layer Context Stack
- RAG 2.0 Pipeline
- Memory Management Strategies
- MCP Architecture
- Security Layers

**Symbolic Concepts** (8 visualizations - $0.96):
- Fourier Transform Kinesthetics
- Nanobot Regimen
- Intelligence Through Crossing
- Hybrid Intelligence

**All images validated at 100% success rate** ✅

---

## 🔧 Claude Code Plugin

Install as native Claude Code plugin:

```bash
mkdir -p ~/.claude/plugins
git clone https://github.com/manutej/nanobanana-repo.git ~/.claude/plugins/nanobanana
cd ~/.claude/plugins/nanobanana
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your GOOGLE_API_KEY to .env
```

See **[claude-plugin.json](claude-plugin.json)** for plugin manifest.

---

## 🛡️ Security

- ✅ API keys stored in `.env` only (gitignored)
- ✅ Pre-commit hooks prevent key exposure
- ✅ Zero keys in code/docs
- ✅ Security rules in [CLAUDE.md](CLAUDE.md)

**Never commit your .env file!**

---

## 📊 Validated Performance

- **18 images generated** (Context + Symbolic)
- **100% success rate** across both test suites
- **Zero rate limit errors**
- **$2.16 total cost**
- **Production-ready quality**

See **[CONTEXT-ENGINEERING-PIPELINE-TEST.md](docs/CONTEXT-ENGINEERING-PIPELINE-TEST.md)** for full test report.

---

## 🤝 Contributing

Contributions welcome! See **[CONTRIBUTING.md](CONTRIBUTING.md)** for guidelines.

---

## 📜 License

MIT License - See **[LICENSE](LICENSE)** for details.

---

## 🙏 Acknowledgments

- Powered by [Google Gemini API](https://ai.google.dev/)
- Async pattern inspired by comonadic extraction
- Research via Context7 MCP

---

**Built for Claude Code users** | Generate production-quality images with ease! 🎨✨
