# Find Topic Like Dan Koe v2.0

<p align="center">
  <a href="README.md">English</a> | <a href="README_CN.md">简体中文</a>
</p>

> A Claude Code plugin for viral topic research combining [Dan Koe](https://x.com/thedankoe)'s methodology with a multi-disciplinary theory arsenal (philosophy, psychology, communication, sociology).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What's New in v2.0

**Multi-Disciplinary Theory Arsenal** - Go beyond basic formulas with deep theoretical frameworks:

- **Philosophy**: Husserl, Heidegger, Nietzsche, Foucault, Levinas, Wittgenstein, Stoicism
- **Psychology**: Jung archetypes, emotional triggers, cognitive biases, Maslow
- **Communication**: Framing theory, attention capture, narrative transportation, AIDA
- **Sociology**: Social identity theory, social comparison, symbolic interactionism

**4 New Advanced Hook Types**:
- Existential Awakening (Heidegger-inspired)
- Value Subversion (Nietzsche-inspired)
- Power Awareness (Foucault-inspired)
- Archetype Activation (Jung-inspired)

**VIRAL Scoring System**: A new evaluation framework measuring Validation/Violation, Identity, Resonance, Attention, and Logic.

---

## Overview

This plugin provides a systematic approach to finding viral content topics by:

1. Analyzing trending content across multiple platforms (Xiaohongshu, Douyin, X/Twitter, WeChat, Zhihu)
2. Applying multi-disciplinary theoretical analysis
3. Generating data-driven topic ideas using Dan Koe's proven formulas + theory enhancement

**Key Features:**

- Multi-platform viral content research
- Dan Koe's 7 core topic formulas + theory enhancement
- Dan Koe's "Triangular Validation" method + multi-disciplinary analysis
- 12 psychological hook types (8 basic + 4 advanced theory-driven)
- Smart 6-dimensional scoring system (upgraded from 4)
- VIRAL scoring methodology
- Theory combination formulas
- Brand persona integration
- Theory focus selection (philosophy/psychology/social/balanced)
- Automated research report generation with theory insights

---

## The VIRAL Content Model

```
┌─────────────────────────────────────────────────────────────┐
│                    VIRAL CONTENT MODEL                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌───────────┐   ┌───────────┐   ┌───────────┐            │
│   │ Philosophy│   │ Psychology │   │Communication│           │
│   │ Existential│ + │  Emotional │ + │  Attention  │          │
│   │  Tension  │   │  Triggers  │   │   Capture   │          │
│   └─────┬─────┘   └─────┬─────┘   └─────┬─────┘            │
│         │               │               │                   │
│         └───────────────┼───────────────┘                   │
│                         ▼                                   │
│               ┌─────────────────┐                          │
│               │    Sociology    │                          │
│               │ Identity & Social│                         │
│               │   Resonance     │                          │
│               └─────────────────┘                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Installation

### Option 1: Install via Claude Code Plugin (Recommended)

```bash
# Add this plugin directly to Claude Code
/plugin install iamzifei/find-topic-like-dankoe-skill
```

### Option 2: Manual Installation

#### Clone and Link

```bash
# Clone the repository
git clone https://github.com/iamzifei/find-topic-like-dankoe-skill.git

# Create the skills directory if it doesn't exist
mkdir -p ~/.claude/skills

# Create a symbolic link to the skill
ln -s /path/to/find-topic-like-dankoe-skill/skills/find-topic/SKILL.md ~/.claude/skills/find-topic/SKILL.md
```

### Verify Installation

```bash
# Check if skill is installed
ls -la ~/.claude/skills/

# Should show find-topic directory or symlink
```

After installation, restart Claude Code or start a new session to load the skill.

---

## Quick Start

```bash
# Basic usage - search for trending content
/find-topic

# With keyword
/find-topic AI programming

# With brand persona
/find-topic skincare --brand=skincare-blogger

# Specific platform
/find-topic indie dev --platform=xiaohongshu

# With theory focus (NEW in v2.0)
/find-topic career growth --theory=philosophy

# Chinese command alias
/选题 AI工具
```

---

## Project Structure

```
find-topic-like-dankoe-skill/
├── .claude-plugin/
│   └── plugin.json           # Plugin manifest
├── skills/
│   └── find-topic/
│       └── SKILL.md          # Main skill definition (v2.0)
├── brands/                    # Brand persona configurations
│   ├── _template.md           # Template for new personas
│   ├── README.md              # Brand configuration guide
│   └── ...                    # Example brand files
├── outputs/                   # Generated research reports
├── theory-arsenal.md          # Theory framework documentation (NEW)
├── README.md                  # English documentation
├── README_CN.md               # Chinese documentation
└── .gitignore
```

---

## Theory Arsenal Quick Reference

### Philosophical Frameworks

| Theorist | Core Concept | Content Application | Hook Template |
|----------|-------------|---------------------|---------------|
| **Husserl** | Epoché, essence intuition | Return to things themselves | "Forget everything you know about X" |
| **Heidegger** | Being-toward-death, authenticity | Existential urgency | "You have Y time left—what are you doing?" |
| **Nietzsche** | Revaluation, will to power | Subvert beliefs | "X is actually a weak person's invention" |
| **Foucault** | Power/knowledge, discipline | Reveal control | "Why X wants you to believe Y" |
| **Levinas** | The Other, responsibility | Relational perspective | "What you owe to X" |
| **Wittgenstein** | Language games | Redefine concepts | "'X' doesn't mean what you think" |
| **Stoicism** | Dichotomy of control | Focus on controllable | "The only thing that matters about X is Y" |

### Psychological Triggers

| Trigger | Intensity | Hook Template |
|---------|-----------|---------------|
| **Fear** | ★★★★★ | "The danger of X you don't know" |
| **Curiosity** | ★★★★★ | "The truth about X is..." |
| **Anger** | ★★★★☆ | "We've all been fooled by X" |
| **Hope** | ★★★★☆ | "It's not too late to X" |
| **Pride** | ★★★★☆ | "Only 1% know about X" |
| **Belonging** | ★★★☆☆ | "If you're a X type person..." |
| **Surprise** | ★★★★☆ | "X is actually Y" |
| **Validation** | ★★★★☆ | "You were right—X is indeed Y" |

### Jung Archetypes

| Archetype | Characteristics | Hook Template |
|-----------|----------------|---------------|
| **Hero** | Courage, transformation | "Your hero's journey starts with X" |
| **Mentor** | Wisdom, guidance | "I wish someone told me Y when X" |
| **Shadow** | Hidden, integration | "That X version of yourself you hate" |
| **Sage** | Truth, insight | "The ancient wisdom about X" |
| **Explorer** | Adventure, freedom | "It's time to explore X" |

---

## The 12 Hook Types

### Basic Hooks (8 types)

| Type | Formula | Example |
|------|---------|---------|
| Pain Point | "Are you still [problem]?" | Are you still trading time for money? |
| Transformation | "From [low] to [high]" | From $3K/month to $100K/year |
| Counter-intuitive | "[Belief] is actually wrong" | Hard work won't make you rich |
| Reveal | "The truth about [Topic]..." | The truth about making millions |
| Listicle | "[N] ways to [goal]" | 5 ways to earn $1M |
| Question | "Why [A] but [B]?" | Why do some people not work but earn millions? |
| Comparison | "Average people [A], experts [B]" | Poor mindset vs Rich mindset |
| Prediction | "In [Year], [prediction]" | In 2026, these 3 types will get rich |

### Advanced Theory-Driven Hooks (4 types) - NEW

| Type | Theory Base | Formula | Example |
|------|-------------|---------|---------|
| **Existential Awakening** | Heidegger | "You have [limited time], yet [waste]" | "You have 4000 weeks to live—how many left?" |
| **Value Subversion** | Nietzsche | "[Virtue] is actually [weakness disguise]" | "Humility is another form of arrogance" |
| **Power Awareness** | Foucault | "Why [authority] wants you to believe [X]" | "Why schools never teach you about money" |
| **Archetype Activation** | Jung | "Your inner [archetype] is calling" | "That entrepreneur inside you—when will you start?" |

---

## Theory Combination Formulas

| Combination | Theory Recipe | Use Case | Template |
|-------------|---------------|----------|----------|
| **Existential Anxiety + Solution** | Heidegger + Stoicism | Life planning | "Life is short, but you only need to focus on this one thing" |
| **Value Subversion + Identity Upgrade** | Nietzsche + Social Identity | Growth breakthrough | "Stop being a good employee—become an entrepreneur" |
| **Power Reveal + Self-Liberation** | Foucault + Jung | Workplace/social critique | "Your procrastination isn't a disease—it's resistance" |
| **Archetype + Hero's Journey** | Jung + Narrative Transport | Inspirational stories | "Everyone is the hero of their own story" |
| **Loss Fear + Urgent Action** | Loss Aversion + Heidegger | Urgent conversion | "You're losing these opportunities every day" |
| **Social Comparison + Identity Leap** | Festinger + Nietzsche | Competitive motivation | "Your peers are already...while you're still..." |

---

## VIRAL Scoring System

```
V (Validation/Violation) - Expectation validation/violation: 1-10
I (Identity) - Identity activation level: 1-10
R (Resonance) - Emotional resonance: 1-10
A (Attention) - Attention capture power: 1-10
L (Logic) - Logical credibility: 1-10

VIRAL Score = (V×1.5 + I×1.2 + R×1.3 + A×1.5 + L×0.5) / 6
Target: ≥ 7.5 for high viral potential
```

---

## Workflow

```
Input (optional)
  ├── Keywords
  ├── Brand persona
  ├── Target platform
  └── Theory focus (NEW)
         ↓
Phase 1: Viral Content Collection
  ├── Xiaohongshu (likes > 10k)
  ├── Douyin (likes > 100k)
  ├── X (engagement > 1k)
  ├── WeChat (reads > 100k)
  └── Zhihu (upvotes > 1k)
         ↓
Phase 2: Multi-Disciplinary Analysis (NEW)
  ├── Basic hook type identification
  ├── Philosophy dimension analysis
  ├── Psychology dimension analysis
  ├── Communication dimension analysis
  └── Sociology dimension analysis
         ↓
Phase 3: Topic Generation (36 topics)
  ├── 3 topics × 8 basic hook types
  └── 3 topics × 4 advanced hook types
         ↓
Phase 4: Smart Filtering (6 dimensions)
  ├── Persona fit (20%)
  ├── Feasibility (15%)
  ├── Differentiation (20%)
  ├── Appeal (20%)
  ├── Theory depth (15%) - NEW
  └── Tension strength (10%) - NEW
         ↓
Phase 5: Output
  ├── Research report (.md)
  ├── Theory pattern analysis
  ├── VIRAL scores
  └── TOP 10 picks with theory insights
```

---

## Command Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--brand=<name>` | Brand persona file name | None |
| `--platform=<name>` | Target platform | All platforms |
| `--count=<n>` | Topics per hook type | 3 |
| `--top=<n>` | Number of top picks | 10 |
| `--theory=<type>` | Theory focus (philosophy/psychology/social/balanced) | balanced |

---

## Brand Persona

Create a file in `/brands/` following the template (`_template.md`). Key fields:

- Brand positioning
- Target audience
- Tone of voice
- Content boundaries (Do's and Don'ts)
- Platform-specific strategies

See `/brands/README.md` for detailed configuration guide.

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## References

### Dan Koe Methodology
- [Dan Koe - How Smart Creators Will Build An Audience In 2025](https://thedankoe.com/letters/the-future-of-creators-how-to-build-an-audience-in-2025/)
- [Dan Koe's AI Content Engine (Podcast)](https://pod.wave.co/podcast/the-startup-ideas-podcast-419dd166-eb67-4971-ab0f-a963c1d70d97/inside-dan-koes-ai-content-engine)
- [Prompt: Generate 50+ Good Content Ideas](https://letters.thedankoe.com/p/prompt-generate-50-good-content-ideas)

### Theory Arsenal
- See `/theory-arsenal.md` for complete theoretical framework documentation

---

## License

MIT License - see [LICENSE](LICENSE) for details.

## Author

- **James** - [GitHub](https://github.com/iamzifei)
