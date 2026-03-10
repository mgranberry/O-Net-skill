# O*NET Database Skill — Setup Guide

## What is O*NET?

**O*NET** (Occupational Information Network) is a comprehensive database of occupational data maintained by the U.S. Department of Labor. It contains detailed information on ~1,000 U.S. occupations including:

- **Skills** required (programming, critical thinking, communication, etc.)
- **Knowledge domains** (computers, mathematics, business, psychology, etc.)
- **Tasks** and responsibilities
- **Work activities** (analysis, decision-making, mentoring, etc.)
- **Education & training** requirements
- **Technology** and tools used
- **Work styles** and values
- **Wages and job outlook**

## Why Use This Skill?

This skill lets AI agents query the O*NET database to:

- **Analyze job roles** — Understand what skills, knowledge, and work activities define a specific occupation
- **Compare occupations** — Find what's common between roles or how they differ
- **Identify skill gaps** — Determine what someone needs to learn to transition between careers
- **Assess AI impact** — Evaluate which occupations are most affected by automation (see example below)
- **Plan hiring** — Identify high-value skills for a particular role
- **Build career development plans** — Understand learning pathways and adjacent roles
- **Conduct labor market research** — Analyze trends, skills demand, and technology adoption by occupation

### Example Use Cases

Agents can leverage this skill for sophisticated analysis:

- **Skill mapping for hiring**: "Find all occupations that require both 'Critical Thinking' and 'Programming' at importance > 4.0"
- **Technology trends**: "Which occupations use Kubernetes? How does that compare to Docker adoption?"
- **Education planning**: "What are the top 5 skills a Business Analyst needs, and what knowledge domains support them?"
- **Career navigation**: "I'm a Systems Administrator. What high-value roles can I transition to without retraining?"

## Setup Guide

This guide covers installation and initial data setup.

## Prerequisites

- **Python**: 3.10 or higher
- **uv**: The Python package manager ([install uv](https://docs.astral.sh/uv/getting-started/installation/))

## Installation

### 1. Clone or Extract This Repository

```bash
git clone <repo-url> onet-skill
cd onet-skill
```

### 2. Download the Database and Build SQLite Index

This is a one-time setup. It downloads all O*NET data files (~40 Excel files) and builds a searchable SQLite database.

```bash
uv run scripts/onet_update.py
```

**What happens:**
- Downloads O*NET database files to `references/`
- Converts them into a single SQLite database: `references/onet.db`
- Records the version in `references/.version`

**Time**: ~2–3 minutes on first run.

**Disk space**: ~500 MB (Excel files + database)

### 3. Verify Installation

```bash
# List available occupations
uv run scripts/onet_search.py --list "engineer"
```

If you see a list of occupations, setup is complete.

## Checking for Updates

The O*NET database is updated periodically by the U.S. Department of Labor.

```bash
# Check if an update is available (no download)
uv run scripts/onet_update.py --check

# Show current local version
uv run scripts/onet_update.py --version

# Download and rebuild if a newer version exists
uv run scripts/onet_update.py
```

## Rebuilding the Database

If the SQLite database becomes corrupted or you want to rebuild without re-downloading:

```bash
uv run scripts/onet_build_db.py
```

## Installing the Skill for AI Agents

### For Claude (via .claude/skills)

```bash
# Copy the skill directory to Claude's skills folder
cp -r . ~/.claude/skills/onet-skill
```

Then reference `onet-skill` in your Claude configuration.

### For Other AI Agents

Each agent has its own skill directory structure. Consult your agent's documentation for the correct path. Common patterns:

- **Anthropic Claude**: `~/.claude/skills/`
- **OpenAI GPT**: `~/.openai/skills/` or similar
- **LangChain**: Typically loaded via path reference in code

The skill is self-contained: copy the entire `onet-skill/` directory to your agent's skills folder.

## Data Location

After setup, the project structure is:

```
onet-skill/
  SKILL.md                  # Skill documentation (for agents)
  README.md                 # This file
  references/
    *.xlsx                  # Raw O*NET Excel files (40 files)
    onet.db                 # SQLite database (searchable index)
    .version                # Current O*NET version
    DATA_DICTIONARY.md      # Schema reference
  scripts/
    onet_search.py          # Search CLI tool
    onet_update.py          # Download/update tool
    onet_build_db.py        # Database builder
```

## Troubleshooting

### "uv: command not found"

Install uv: https://docs.astral.sh/uv/getting-started/installation/

### "ModuleNotFoundError: No module named 'openpyxl'"

Run `uv run scripts/onet_update.py` again. Dependencies are installed automatically via uv.

### "references/onet.db" not found

Run `uv run scripts/onet_update.py` to download data and build the database.

### Large download stuck

The download includes 40 Excel files (~300 MB). On slow connections, this can take 5–10 minutes. The script will resume if interrupted.

## License

O*NET data is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) by the U.S. Department of Labor/Employment and Training Administration (USDOL/ETA).

Scripts in this repository are provided as-is for working with O*NET data.

## Next Steps

- Load `SKILL.md` into your agent for query documentation
- See `references/DATA_DICTIONARY.md` for database schema details
- Run `uv run scripts/onet_search.py --help` for search options
