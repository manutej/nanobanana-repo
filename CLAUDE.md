# Claude Code Global Configuration

**Master Reference** - Global configuration providing system-wide settings, skills, agents, commands, and workflows.

---

## 🚨 CRITICAL SECURITY RULES - API KEY PROTECTION

**ABSOLUTE RULES - NEVER VIOLATE UNDER ANY CIRCUMSTANCES**:

### Rule 1: NEVER Accept API Keys in Chat
- ❌ **REFUSE** if user pastes an API key in chat messages
- ❌ **STOP** immediately and warn user that chat history is permanent
- ✅ **INSTRUCT** user to add API keys directly to `.env` file manually
- ✅ **NEVER** use API keys shared in chat (they are now compromised)

### Rule 2: NEVER Output API Keys
- ❌ **NEVER** include API keys in responses, examples, or documentation
- ❌ **NEVER** echo API keys from environment variables
- ❌ **NEVER** log API keys (even partial keys)
- ❌ **NEVER** include API keys in commit messages
- ❌ **NEVER** use real API keys in code examples or tests

### Rule 3: ONLY Use .env for API Keys
- ✅ **ONLY** location for real API keys: `.env` file
- ✅ **ALWAYS** verify `.env` is in `.gitignore`
- ✅ **ALWAYS** use placeholders in examples: `your_api_key_here`
- ✅ **ALWAYS** use `os.getenv()` to load from environment

### Rule 4: Pre-Commit Validation
- ✅ **ALWAYS** scan files before committing for API key patterns
- ✅ **BLOCK** commits containing `AIza`, `sk-`, `ghp_`, or other API key prefixes
- ✅ **WARN** user if suspicious patterns detected

### Secure API Key Workflow
```bash
# ✅ CORRECT: User adds key directly to .env
echo "GOOGLE_API_KEY=AIza..." >> .env

# ❌ WRONG: User shares key in chat
"Here's my new API key: AIza..."  # REFUSE THIS!
```

**If User Shares API Key in Chat**:
1. ⛔ **STOP** - Do not use the key
2. ⚠️ **WARN** - "API key exposed in chat history - it is now compromised"
3. 📋 **INSTRUCT** - "Please revoke this key and generate a new one"
4. 📝 **GUIDE** - "Add the NEW key directly to .env file manually"

---

**Quick Links**:
- 📖 [Quick Start](.claude/docs/QUICK-START.md) - Get started quickly
- ⚙️ [Settings](.claude/docs/SETTINGS.md) - Configuration details
- 🔄 [Actualization](.claude/docs/ACTUALIZATION.md) - Sync guide
- 📋 [Changelog](.claude/docs/CHANGELOG.md) - Change history
- 🏗️ [Architecture](.claude/docs/ARCHITECTURE.md) - System design

---

## Current Inventory

**Last Updated**: 2025-11-15T12:35:00Z

| Category | Count | Location |
|----------|-------|----------|
| **Skills** | 101 | `~/.claude/skills/` |
| **Agents** | 46 | `~/.claude/agents/` |
| **Commands** | 62 | `~/.claude/commands/` |
| **Workflows** | 21 | `~/.claude/workflows/` |
| **MCP Servers** | 10 | Context7, Linear, Sequential-Thinking, ArXiv, Wolfram, Diagram-Bridge, Crush, Pandoc, Figma, Geocoding |

**Total Resources**: 240 items available globally

**Latest Addition**: **moe** (Mixture of Experts) - Complete orchestration specification integrating skill + agents + commands for complex, high-stakes decision-making through multi-expert analysis with parallel execution, 4 convergence methods, and confidence-scored recommendations (5,842 lines, production-validated from MERCURIO project)

**Agent Structure Note**: Multi-file agents (MARS, MERCURIO, HEKAT) store documentation in `{agent-name}/docs/` subdirectories. Main agent definitions remain in the root agents/ folder with proper YAML frontmatter.

---

## Essential Commands

```bash
/startup             # Initialize environment (Explanatory mode + statusline)
/actualize           # Sync all configurations
/ctx7 <library>      # Library documentation lookup
/workflows           # List and execute workflows
/crew                # Agent discovery and management
/hekat               # L1-L7 orchestration builder
```

**See**: [QUICK-START.md](.claude/docs/QUICK-START.md) for complete command reference

---

## Documentation Index

Detailed documentation organized by topic in `.claude/docs/`:

### Getting Started
- **[QUICK-START.md](.claude/docs/QUICK-START.md)** - Essential commands, first skill, troubleshooting
- **[SETTINGS.md](.claude/docs/SETTINGS.md)** - Global/project settings, MCP configuration

### Reference Materials
- **[AGENT-REFERENCE.md](.claude/docs/AGENT-REFERENCE.md)** - 39 agents, workflows, selection matrix
- **[SKILLS-CATALOG.md](.claude/docs/SKILLS-CATALOG.md)** - 81 skills by category, usage patterns
- **[DIRECTORY-STRUCTURE.md](.claude/docs/DIRECTORY-STRUCTURE.md)** - File organization, golden rules

### Guides
- **[ACTUALIZATION.md](.claude/docs/ACTUALIZATION.md)** - Complete sync guide, patterns, examples
- **[TASK-RELAY-GUIDE.md](.claude/docs/TASK-RELAY-GUIDE.md)** - Token discipline, orchestration patterns
- **[SKILLS-USAGE-GUIDE.md](.claude/docs/SKILLS-USAGE-GUIDE.md)** - Auto vs explicit, progressive disclosure

### Architecture
- **[ARCHITECTURE.md](.claude/docs/ARCHITECTURE.md)** - Three-layer model, Task Relay, HEKAT DSL
- **[INTEGRATION_LAYER.md](.claude/docs/INTEGRATION_LAYER.md)** - Cross-system integration patterns

### History
- **[CHANGELOG.md](.claude/docs/CHANGELOG.md)** - Complete change history with timestamps

---

## Recent Highlights

### Barque + Pop Email Integration (2025-11-01 08:35)
- **New workflow**: Markdown → Dual-theme PDF → Email delivery
- Validated with 77K+ words across 2 research packages
- 4 PDFs generated (8.4 MB) and delivered successfully
- Documentation: `LUXOR/PROJECTS/BARQUE/consciousness.md`
- Command: `/pop-mail` updated with real-world patterns

### F* Meta-Prompting Framework (2025-11-01)
- 7-level categorical framework (L1 Novice → L7 Genius)
- 42 verification examples, 7 categorical proofs
- Location: `LUXOR/PROJECTS/fstar-framework/`

### New Skills (2025-11-01)
- **elm-development** (109.6 KB) - Functional web development
- **fstar-verification** (82 KB) - Formal verification with dependent types

**See**: [CHANGELOG.md](.claude/docs/CHANGELOG.md) for complete history

---

## Orchestration Specifications

### MOE (Mixture of Experts) - Complete Specification Pattern

**MOE** represents a complete orchestration specification that integrates **skill + agents + commands** for complex, high-stakes decision-making through multi-expert analysis.

**When to Invoke**: `Skill: "moe"` or `/mercurio`

**What "moe" Orchestrates**:

| Component | Resource | Purpose |
|-----------|----------|---------|
| **Skill** | `moe` (5,842 lines) | Complete MOE methodology, convergence algorithms, templates |
| **Agents** | `mercurio-orchestrator`, `MERCURIO`, `mercurio-synthesizer`, `mercurio-pragmatist` | Expert analysis across mental/physical/spiritual planes |
| **Commands** | `/mercurio` | Quick invocation of MOE analysis |
| **Workflows** | `moe-*.yaml` | Pre-configured decision workflows (API, architecture, database) |

**Core Capabilities**:
- **7-Stage Process**: Frame → Select → Diverge (parallel) → Document → Converge → Decide → Monitor
- **4 Convergence Methods**: Weighted voting, Consensus building, Delphi method, Dialectical synthesis
- **6 Confidence Thresholds**: 90%+ (execute), 80-90% (plan), 70-80% (prototype), 60-70% (spike), 50-60% (gather data), <50% (halt)
- **Expert Selection**: 3-7 diverse agents with domain-weighted voting

**Usage Pattern**:
```bash
# Invoke complete MOE specification
Skill: "moe"

# Or use slash command
/mercurio

# Example decision
"Use moe to analyze: Should we migrate to microservices?
Launch parallel analysis with project-orchestrator (architecture),
practical-programmer (pragmatism), and devops-specialist (operations).
Generate convergence document with confidence-scored recommendation."
```

**Key Innovation**: Single invocation (`moe`) triggers entire ecosystem - parallel expert launch, convergence synthesis, confidence scoring, and actionable recommendations. No need to manually coordinate skill + agents + commands.

**Production-Validated**: From MERCURIO project's paper2agent L7 standard, demonstrating 2000x ROI by preventing $100k+ mistakes through systematic multi-expert analysis.

---

## Quick Reference

### Architecture
**Agent + Skills + Virtual Machine** = Comprehensive development assistance

- **Agent Configuration**: System prompt + skills + MCP servers
- **Virtual Machine**: Bash, Python, Node.js runtimes
- **File System**: `~/.claude/` configuration directory

### Best Practices
- Skills: Auto-select by default; explicit reference when needed
- Configuration: Global in `~/.claude/`, project in `.claude/`
- Workflow: `create_new_item && /actualize` keeps everything synchronized

**See**: [QUICK-START.md](.claude/docs/QUICK-START.md) for detailed practices

---

## Workspace Hygiene

**Core Principle**: Keep working directories (LUXOR/, CETI/, etc.) clean and organized at all times.

### Directory Organization Rules

| Location | Purpose | What Belongs |
|----------|---------|--------------|
| `LUXOR/`, `CETI/` root | Clean workspace | Active projects, README, SETUP only |
| `PROJECT/docs/` | Documentation | Specs, guides, architecture, tutorials |
| `PROJECT/logs/` | Operational logs | Cleanup reports, execution logs, debug output |
| `docs/` (global) | Global docs | Cross-project documentation |
| `logs/` (global) | Global logs | Workspace-level operational logs |
| `archive/` | Historical | Old files, deprecated artifacts, backups |

### File Placement Guidelines

**Always organize immediately**:
- 📄 **Documentation** → `{PROJECT}/docs/` (or `docs/` if global)
- 📊 **Logs & Reports** → `{PROJECT}/logs/` (or `logs/` if global)
- 🗑️ **Temporary files** → Delete or `archive/temp-files/`
- 📦 **Old artifacts** → `archive/{category}/`
- 🎯 **Project-specific** → Never in root, always in project directory

**Quick Test**: If a file has a project name in its filename, it belongs in that project's directory.

### Example Organization

```bash
# ✅ Well-organized workspace
LUXOR/
├── .claude/              # Claude configuration
├── PROJECTS/
│   └── BARQUE/
│       ├── docs/         # Project documentation
│       ├── logs/         # Project logs
│       ├── src/          # Source code
│       └── README.md     # Project readme
├── djed/                 # Another project
│   ├── docs/
│   ├── logs/
│   └── src/
├── docs/                 # Global documentation
├── logs/                 # Global operational logs
├── archive/              # Historical artifacts
├── README.md             # Workspace readme
└── SETUP.md              # Setup instructions

# ❌ Cluttered workspace (needs cleanup)
LUXOR/
├── BARQUE-SPEC.md       # → PROJECTS/BARQUE/docs/
├── DJED-NOTES.md        # → djed/docs/
├── cleanup-log.txt      # → logs/
├── old-version.md       # → archive/
└── temp-file.json       # → delete or archive/
```

### Maintenance Commands

```bash
/cleanup              # Organize and clean workspace
/cleanup --report     # Check workspace status
/actualize            # Sync Claude configuration
```

**Frequency**:
- 🔄 **After major work**: Run `/cleanup` to organize new files
- 📅 **Weekly**: Quick `/cleanup --report` check
- 🧹 **Monthly**: Full `/cleanup --full` deep clean

**See**: Run `/cleanup` for detailed workspace hygiene guidelines

---

## File Locations

### Global Configuration
```
~/.claude/
├── CLAUDE.md                    # This file (master reference)
├── settings.json                # Global settings
├── docs/                        # Documentation (9 files)
│   ├── QUICK-START.md
│   ├── SETTINGS.md
│   ├── ACTUALIZATION.md
│   ├── CHANGELOG.md
│   ├── ARCHITECTURE.md
│   ├── AGENT-REFERENCE.md
│   ├── SKILLS-CATALOG.md
│   ├── TASK-RELAY-GUIDE.md
│   ├── SKILLS-USAGE-GUIDE.md
│   ├── DIRECTORY-STRUCTURE.md
│   └── INTEGRATION_LAYER.md
├── skills/                      # 81 skill directories
├── agents/                      # 48 agent definitions
├── commands/                    # 55 slash commands
└── workflows/                   # 19 workflow YAML files
```

### Project Configuration
```
.claude/
├── CLAUDE.md                    # Project reference (synced from global)
├── settings.json                # Project-specific settings
├── docs/                        # Same docs as global
├── skills/                      # Project + global skills
├── agents/                      # Project + global agents
├── commands/                    # Project + global commands
└── workflows/                   # Project + global workflows
```

**See**: [DIRECTORY-STRUCTURE.md](.claude/docs/DIRECTORY-STRUCTURE.md) for complete hierarchy

---

## Resources

- **Claude Code Docs**: https://docs.claude.com/en/docs/claude-code
- **Skills Blog**: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- **Local Documentation**: `.claude/docs/` directory (11 reference files)

---

## Summary

**100 Skills** + **46 Agents** + **59 Commands** + **19 Workflows** + **10 MCP Servers** = **234 total resources**

Comprehensive development assistance via **Agent + Skills + Virtual Machine** architecture.

---

**Status**: All systems synchronized ✅
**Last Actualized**: 2025-11-14T00:15:00Z
**Recent Changes**: Added 4 FP skills (purify, fp-ts, typescript-fp, functional-programming) ported from Claude.ai
**Memory Footprint**: Optimized (30% reduction via distributed documentation)

---

*For detailed information, consult the documentation index above. Each doc file provides focused, comprehensive coverage of its topic.*
