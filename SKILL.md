# O*NET Database Navigation Skill

## Overview

The O\*NET (Occupational Information Network) database contains standardized descriptors on ~1,000 occupations covering the entire U.S. economy. Data lives in `references/` as both Excel (`.xlsx`) source files and a SQLite database (`references/onet.db`) with FTS5 full-text search for fast querying. The current version is tracked in `references/.version`.

Licensed under [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/).

---

## Key Concept: O\*NET-SOC Codes

Every occupation has a unique **O\*NET-SOC Code** (format: `XX-XXXX.XX`, e.g., `15-1252.00` for "Software Developers"). This code is the **primary key** linking all files together. The master list lives in `Occupation Data.xlsx`.

**Parent vs. child codes:** Codes ending in `.00` are sometimes parent categories (e.g., `15-2051.00` "Data Scientists") with `.01`/`.02` child codes for specialized roles (e.g., `15-2051.01` "Business Intelligence Analysts"). About 119 parent codes have **no skills, knowledge, or abilities data** — the rated data lives only on their children. The search script warns when this happens and lists the child codes. When querying directly, use `LIKE 'XX-XXXX%'` to find all variants.

---

## File Inventory & Schema

### Core Occupation File

| File | Rows | Description |
|------|------|-------------|
| **Occupation Data.xlsx** | 1,016 | Master list of all occupations with SOC code, title, and description |

**Columns:** `O*NET-SOC Code`, `Title`, `Description`

This is the starting point for any lookup. Search by title or description to find an O\*NET-SOC Code, then use that code to pull data from all other files.

---

### Worker Characteristics

| File | Rows | Description |
|------|------|-------------|
| **Abilities.xlsx** | 92,976 | Cognitive, psychomotor, physical, and sensory abilities rated per occupation |
| **Interests.xlsx** | 8,307 | Holland/RIASEC interest profiles per occupation |
| **Work Styles.xlsx** | 37,422 | Personality traits/work styles (e.g., Innovation, Persistence) per occupation |
| **Work Values.xlsx** | 7,866 | Work value dimensions (Achievement, Independence, etc.) per occupation |

**Abilities/Skills/Knowledge common schema:**
`O*NET-SOC Code`, `Title`, `Element ID`, `Element Name`, `Scale ID`, `Scale Name`, `Data Value`, `N`, `Standard Error`, `Lower CI Bound`, `Upper CI Bound`, `Recommend Suppress`, `Not Relevant`, `Date`, `Domain Source`

**Interests schema:** `O*NET-SOC Code`, `Title`, `Element ID`, `Element Name`, `Scale ID`, `Scale Name`, `Data Value`, `Date`, `Domain Source`

**Work Styles schema:** `O*NET-SOC Code`, `Title`, `Element ID`, `Element Name`, `Scale ID`, `Scale Name`, `Data Value`, `Date`, `Domain Source`

**Work Values schema:** `O*NET-SOC Code`, `Title`, `Element ID`, `Element Name`, `Scale ID`, `Scale Name`, `Data Value`, `Date`, `Domain Source`

---

### Worker Requirements

| File | Rows | Description |
|------|------|-------------|
| **Knowledge.xlsx** | 59,004 | Knowledge domains rated per occupation (e.g., Mathematics, English Language) |
| **Skills.xlsx** | 62,580 | Skills rated per occupation (e.g., Critical Thinking, Programming) |

Both use the **15-column schema** (same as Abilities above).

---

### Experience Requirements

| File | Rows | Description |
|------|------|-------------|
| **Education, Training, and Experience.xlsx** | 37,125 | Education/training/experience percent-frequency data per occupation |
| **Education, Training, and Experience Categories.xlsx** | 41 | Category lookup (e.g., Category 1 = "Less than a High School Diploma") |
| **Job Zones.xlsx** | 923 | Maps each occupation to a Job Zone (1-5 preparation level) |
| **Job Zone Reference.xlsx** | 4 | Describes each Job Zone's experience, education, and training requirements |

**Education schema:** `O*NET-SOC Code`, `Title`, `Element ID`, `Element Name`, `Scale ID`, `Scale Name`, `Category`, `Data Value`, `N`, `Standard Error`, `Lower CI Bound`, `Upper CI Bound`, `Recommend Suppress`, `Date`, `Domain Source`

**Job Zones schema:** `O*NET-SOC Code`, `Title`, `Job Zone`, `Date`, `Domain Source`

**Job Zone Reference schema:** `Job Zone`, `Name`, `Experience`, `Education`, `Job Training`, `Examples`, `SVP Range`

---

### Occupational Requirements

| File | Rows | Description |
|------|------|-------------|
| **Work Activities.xlsx** | 73,308 | Generalized work activities rated per occupation |
| **Work Context.xlsx** | 297,676 | Work environment conditions per occupation (categorical data) |
| **Task Statements.xlsx** | 18,796 | Specific task descriptions per occupation |
| **Task Ratings.xlsx** | 161,559 | Task frequency/importance ratings per occupation |

**Work Activities schema:** Same 15-column schema as Abilities.

**Work Context schema:** `O*NET-SOC Code`, `Title`, `Element ID`, `Element Name`, `Scale ID`, `Scale Name`, `Category`, `Data Value`, `N`, `Standard Error`, `Lower CI Bound`, `Upper CI Bound`, `Recommend Suppress`, `Not Relevant`, `Date`, `Domain Source` (16 columns — adds `Category`)

**Task Statements schema:** `O*NET-SOC Code`, `Title`, `Task ID`, `Task`, `Task Type`, `Incumbents Responding`, `Date`, `Domain Source`

**Task Ratings schema:** `O*NET-SOC Code`, `Title`, `Task ID`, `Task`, `Scale ID`, `Scale Name`, `Category`, `Data Value`, `N`, `Standard Error`, `Lower CI Bound`, `Upper CI Bound`, `Recommend Suppress`, `Date`, `Domain Source`

---

### Occupation-Specific Information

| File | Rows | Description |
|------|------|-------------|
| **Technology Skills.xlsx** | 32,773 | Software/technology used per occupation (e.g., Python, SAP) |
| **Tools Used.xlsx** | 41,662 | Physical tools/equipment used per occupation |
| **Emerging Tasks.xlsx** | 328 | New/emerging tasks for occupations |
| **Alternate Titles.xlsx** | 57,543 | Alternative job titles per occupation |
| **Sample of Reported Titles.xlsx** | 7,953 | Job titles reported by incumbents |
| **Related Occupations.xlsx** | 18,460 | Related/similar occupations with relatedness tiers |

**Technology Skills schema:** `O*NET-SOC Code`, `Title`, `Example`, `Commodity Code`, `Commodity Title`, `Hot Technology`, `In Demand`

- `Hot Technology` = "Y" means high-demand in job postings
- `In Demand` = "Y" means growing demand

**Tools Used schema:** `O*NET-SOC Code`, `Title`, `Example`, `Commodity Code`, `Commodity Title`

**Alternate Titles schema:** `O*NET-SOC Code`, `Title`, `Alternate Title`, `Short Title`, `Source(s)`

**Related Occupations schema:** `O*NET-SOC Code`, `Title`, `Related O*NET-SOC Code`, `Related Title`, `Relatedness Tier`, `Index`

---

### Reference & Crosswalk Files

| File | Rows | Description |
|------|------|-------------|
| **Content Model Reference.xlsx** | 630 | Maps Element IDs to names/descriptions (the taxonomy hierarchy) |
| **Scales Reference.xlsx** | 31 | Defines all rating scales (ID, Name, Min, Max) |
| **Level Scale Anchors.xlsx** | 483 | Anchor descriptions for level scales |
| **UNSPSC Reference.xlsx** | 4,264 | Product/service classification codes (for Technology Skills / Tools Used) |
| **IWA Reference.xlsx** | 332 | Intermediate Work Activity definitions |
| **DWA Reference.xlsx** | 2,087 | Detailed Work Activity definitions |
| **Tasks to DWAs.xlsx** | 23,850 | Maps specific tasks to Detailed Work Activities |
| **Task Categories.xlsx** | 7 | Category descriptions for task frequency ratings |
| **Work Context Categories.xlsx** | 281 | Category descriptions for work context items |

### Interest Reference Files

| File | Rows | Description |
|------|------|-------------|
| **RIASEC Keywords.xlsx** | 75 | Action/object keywords for each RIASEC interest type |
| **Basic Interests to RIASEC.xlsx** | 53 | Maps basic interests to RIASEC dimensions |
| **Interests Illustrative Activities.xlsx** | 188 | Example activities for each interest type |
| **Interests Illustrative Occupations.xlsx** | 186 | Example occupations for each interest type |

### Cross-Domain Linkage Files

| File | Rows | Description |
|------|------|-------------|
| **Abilities to Work Activities.xlsx** | 381 | Which abilities are used in which work activities |
| **Abilities to Work Context.xlsx** | 139 | Which abilities relate to which work contexts |
| **Skills to Work Activities.xlsx** | 232 | Which skills are used in which work activities |
| **Skills to Work Context.xlsx** | 96 | Which skills relate to which work contexts |

### Data Collection Metadata

| File | Rows | Description |
|------|------|-------------|
| **Occupation Level Metadata.xlsx** | 32,202 | Survey methodology data per occupation |
| **Survey Booklet Locations.xlsx** | 211 | Survey item numbers for content model elements |

---

## Understanding Rating Scales

Check `Scales Reference.xlsx` for all scale definitions. Key scales:

| Scale ID | Scale Name | Min | Max | Used In |
|----------|-----------|-----|-----|---------|
| IM | Importance | 1 | 5 | Knowledge, Skills, Abilities, Work Activities |
| LV | Level | 0 | 7 | Knowledge, Skills, Abilities, Work Activities |
| EX | Extent | 1 | 7 | Work Values |
| OI | Occupational Interests | 1 | 7 | Interests |
| CX | Context | varies | varies | Work Context |
| DR | Distinctiveness Rank | varies | varies | Work Styles |

Most rated files contain **two rows per element per occupation**: one for `IM` (Importance) and one for `LV` (Level). Filter by `Scale ID` to get the measure you want.

---

## Content Model Element ID Hierarchy

Element IDs follow a hierarchical dot notation defined in `Content Model Reference.xlsx`:

```
1           Worker Characteristics
  1.A         Abilities
    1.A.1       Cognitive Abilities
      1.A.1.a     Verbal Abilities
        1.A.1.a.1   Oral Comprehension
  1.B         Interests
  1.C         Work Values (Note: stored as 1.B.2 in the data)
  1.D         Work Styles
2           Worker Requirements
  2.A         Skills
    2.A.1       Basic Skills
    2.A.2       Cross-Functional Skills
  2.C         Knowledge
  2.D         Education
4           Occupational Requirements
  4.A         Work Activities
    4.A.1       Generalized Work Activities
  4.C         Work Context
```

---

## SQLite Database

All data is indexed in `references/onet.db` for fast querying. The search script uses this exclusively — no xlsx parsing at runtime.

**Table naming:** snake_case of xlsx filename (e.g., `Occupation Data.xlsx` -> `occupation_data`, `Technology Skills.xlsx` -> `technology_skills`). Query `_file_map` for the full mapping.

**Column naming:** snake_case (e.g., `O*NET-SOC Code` -> `o_net_soc_code`, `Data Value` -> `data_value`).

**Indices:** B-tree on `o_net_soc_code`, `element_id`, `scale_id`, `task_id`, `commodity_code` where applicable.

**Full-text search (FTS5):**
- `occupation_fts` — search occupation titles and descriptions
- `alternate_titles_fts` — search alternate job titles

**Metadata tables:**
- `_metadata` — key/value pairs (`version`, `build_date`)
- `_file_map` — maps original xlsx filenames to table names

### Direct SQL Examples

```sql
-- FTS5 keyword search for occupations
SELECT * FROM occupation_fts WHERE occupation_fts MATCH 'machine learning';

-- Top skills by importance for an occupation
SELECT element_name, data_value FROM skills
WHERE o_net_soc_code = '15-1252.00' AND scale_id = 'IM'
ORDER BY CAST(data_value AS REAL) DESC LIMIT 10;

-- Hot technologies across all occupations
SELECT DISTINCT example, commodity_title FROM technology_skills
WHERE hot_technology = 'Y' ORDER BY example;

-- Database version
SELECT value FROM _metadata WHERE key = 'version';
```

To rebuild the database from xlsx files:

```bash
uv run scripts/onet_build_db.py
```

---

## Common Query Patterns

These patterns work with both the search script (recommended) and direct SQL on `references/onet.db`.

### Find an occupation
```bash
uv run scripts/onet_search.py --list "software"
```
Or via SQL:
```sql
SELECT * FROM occupation_fts WHERE occupation_fts MATCH 'software';
```

### Get all skills for an occupation
```bash
uv run scripts/onet_search.py --code 15-1252.00 --sections skills
```
Or via SQL:
```sql
SELECT element_name, data_value FROM skills
WHERE o_net_soc_code = '15-1252.00' AND scale_id = 'IM'
ORDER BY CAST(data_value AS REAL) DESC;
```

### Get technology skills
```bash
uv run scripts/onet_search.py --code 15-1252.00 --sections technology
```
Or via SQL:
```sql
SELECT example, commodity_title, hot_technology FROM technology_skills
WHERE o_net_soc_code = '15-1252.00' ORDER BY hot_technology DESC;
```

### Find related occupations
```bash
uv run scripts/onet_search.py --code 15-1252.00 --sections related
```

### Get education requirements
```bash
uv run scripts/onet_search.py --code 15-1252.00 --sections education
```

---

## Updating the Database

A Python script at `scripts/onet_update.py` checks for new O\*NET releases, downloads updated files, and automatically rebuilds the SQLite database. The current version is tracked in `references/.version`.

```bash
# Check current local version
uv run scripts/onet_update.py --version

# Check if a newer version is available (no download)
uv run scripts/onet_update.py --check

# Update to the latest version (downloads all 40 files)
uv run scripts/onet_update.py

# Force re-download of the current version
uv run scripts/onet_update.py --force

# Manually set the version (e.g., after a manual download)
uv run scripts/onet_update.py --set-version 30.2
```

The script detects the latest version via the O\*NET RSS feed, falling back to scraping the database page. Downloads are atomic (temp file + rename) and the version file is only updated after all files download successfully. The SQLite database is rebuilt automatically after a successful download.

---

## Data Dictionary

A detailed reference for all 40 `.xlsx` files is available at `references/DATA_DICTIONARY.md`. It covers column semantics, data types, relationships between files, and sample values for deeper exploration.

---

## Using the Search Script

A Python script at `scripts/onet_search.py` provides command-line access to the database.

### Prerequisites

The script declares its dependencies inline via [PEP 723](https://peps.python.org/pep-0723/), so `uv run` handles everything automatically — no venv or install steps needed.

```bash
uv run scripts/onet_search.py "software developer"
```

### Basic Usage

```bash
# Search for an occupation by keyword (outputs Markdown by default)
uv run scripts/onet_search.py "software developer"

# Output as JSON instead
uv run scripts/onet_search.py "software developer" --format json

# Save to a file
uv run scripts/onet_search.py "software developer" -o report.md
uv run scripts/onet_search.py "software developer" --format json -o report.json

# Search by exact O*NET-SOC code
uv run scripts/onet_search.py --code 15-1252.00

# Limit which sections to include
uv run scripts/onet_search.py "nurse" --sections skills knowledge tasks

# List all available occupations matching a keyword
uv run scripts/onet_search.py --list "engineer"
```

### Output Sections

The report includes (when available):

1. **Occupation Summary** — Title, SOC code, description, job zone
2. **Knowledge** — Top knowledge domains by importance
3. **Skills** — Top skills by importance
4. **Abilities** — Top abilities by importance
5. **Work Activities** — Top work activities by importance
6. **Technology Skills** — Software/technology used (hot tech flagged)
7. **Tasks** — Core task statements
8. **Education** — Education/training requirements
9. **Work Styles** — Personality/work style traits
10. **Work Values** — Work value dimensions
11. **Work Context** — Work environment characteristics
12. **Related Occupations** — Similar/related occupations
13. **Alternate Titles** — Other job titles for this role

### Available `--sections` Filters

`knowledge`, `skills`, `abilities`, `activities`, `technology`, `tasks`, `education`, `styles`, `values`, `context`, `related`, `titles`, `emerging_tasks`, `interests`, `tools`, `task_ratings`

#### New Sections (Enhanced in v0.2)

- **`emerging_tasks`** — New/emerging job responsibilities (as of 08/2025), identified by occupational experts and incumbents. Helps identify future skill demand before widespread adoption.

- **`interests`** — RIASEC personality-occupation alignment scores (Realistic, Investigative, Artistic, Conventional, Enterprising, Social). Useful for career counseling and personality-role fit assessment.

- **`tools`** — Physical and digital equipment/tools used in the occupation (distinct from "technology" skills). Includes machinery, software, and specialized equipment.

- **`task_ratings`** — Task frequency ratings with statistical confidence intervals. Shows not just *what* tasks are done, but *how often* (daily, weekly, yearly, etc.) with 95% confidence bounds and sample size. Higher statistical rigor than simple task lists.

### Examples

```bash
# Full report for a data scientist
uv run scripts/onet_search.py "data scientist" -o data_scientist.md

# Just skills and tech for a nurse
uv run scripts/onet_search.py "registered nurse" --sections skills technology

# JSON for programmatic use
uv run scripts/onet_search.py --code 29-1141.00 --format json -o nurse.json

# Browse available engineering occupations
uv run scripts/onet_search.py --list "engineer"
```
