# O*NET Hidden Tables Reference

This document describes the 42 O*NET database tables that are **not directly exposed** through the main `onet_search.py` command-line interface but are available for advanced queries via raw SQL.

These tables contain high-value occupational data for specialized analysis: skill relationships, personality-occupation alignment, equipment/tools data, and quality metrics.

---

## Quick Reference: High-Value Hidden Tables

| Table | Rows | Use Case |
|-------|------|----------|
| `emerging_tasks` | 328 | New job responsibilities being added (future-focused roles) |
| `interests` | 8,307 | RIASEC personality-occupation alignment (career counseling) |
| `tools_used` | 41,662 | Physical & digital equipment/tools per occupation |
| `task_ratings` | 161,559 | Task frequency ratings with confidence intervals (statistical credibility) |
| `level_scale_anchors` | 483 | Interpretive examples for ability ratings (what "Level 3" actually means) |
| `occupation_level_metadata` | 32,202 | Data quality metrics (collection mode, completeness, confidence) |
| `skills_to_work_activities` | — | Relationship: which skills are used in which activities |
| `abilities_to_work_activities` | — | Relationship: which abilities are used in which activities |

---

## Detailed Table Schemas & Examples

### 1. **emerging_tasks** (328 rows)

New/emerging tasks being added to occupations as of 08/2025. Marked by occupational experts and incumbents.

**Schema:**
```sql
o_net_soc_code TEXT      -- Occupation code (e.g., "11-2022.00")
title          TEXT      -- Occupation title
task           TEXT      -- New task description
category       TEXT      -- Classification ("New", etc.)
original_task_id INTEGER -- References original task if modified
original_task  TEXT      -- Previous task version (if update)
date           TEXT      -- Dated 08/2025 in current database
domain_source  TEXT      -- "Occupational Expert" or "Incumbent"
```

**Example:**
```sql
SELECT task, domain_source FROM emerging_tasks 
WHERE o_net_soc_code = '11-2022.00';

-- Output:
-- Coach staff on sales tactics. | Occupational Expert
-- Establish and monitor staff's sales goals. | Occupational Expert
```

**Use Cases:**
- Identify occupations gaining new responsibilities (skill evolution)
- Anticipate future skill demand before widespread adoption
- Track how job roles are changing in real-time

---

### 2. **interests** (8,307 rows)

RIASEC (Realistic, Investigative, Artistic, Conventional, Enterprising, Social) personality-occupation alignment scores. Psychometric data linking occupations to occupational interest dimensions.

**Schema:**
```sql
o_net_soc_code TEXT   -- Occupation code
title          TEXT   -- Occupation title
element_id     TEXT   -- RIASEC dimension code (e.g., "1.B.1.a" = Realistic)
element_name   TEXT   -- RIASEC name (Realistic, Investigative, etc.)
scale_id       TEXT   -- "OI" (Occupational Interests)
scale_name     TEXT   -- "Occupational Interests" or "Occupational Interest High-Point"
data_value     REAL   -- Score (0–10 typically; higher = stronger alignment)
date           TEXT   -- Collection date (02/2026 in current database)
domain_source  TEXT   -- "Machine Learning/Expert" or "Incumbent"
```

**Example:**
```sql
SELECT element_name, data_value FROM interests
WHERE o_net_soc_code = '15-1252.00'  -- Software Developer
ORDER BY data_value DESC;

-- Output:
-- Investigative | 6.05
-- Second Interest High-Point | 6.00
-- Conventional | 5.62
-- Realistic | 3.61
```

**Use Cases:**
- Career counseling: "What occupations match my RIASEC profile?"
- Skill/education planning: Identify roles aligned with personality
- Occupational clustering: Group roles by personality requirements
- Workforce assessment: Evaluate personality-role fit for hiring

**RIASEC Dimensions:**
- **Realistic (R)**: Hands-on work, tools, machinery, physical activity
- **Investigative (I)**: Analysis, research, thinking, solving complex problems
- **Artistic (A)**: Creativity, aesthetics, self-expression
- **Conventional (C)**: Organization, systems, order, rules, data
- **Enterprising (E)**: Leadership, persuasion, influence, entrepreneurship
- **Social (S)**: Helping, teaching, supporting others

---

### 3. **tools_used** (41,662 rows)

Physical and digital equipment/tools required for each occupation. Distinct from "technology_skills"—includes physical tools, machinery, and software.

**Schema:**
```sql
o_net_soc_code  TEXT    -- Occupation code
title           TEXT    -- Occupation title
example         TEXT    -- Specific tool name (e.g., "Kubernetes", "Welding torch")
commodity_code  INTEGER -- UNSPSC commodity classification code
commodity_title TEXT    -- Commodity category (e.g., "Application servers")
```

**Example:**
```sql
SELECT example, commodity_title FROM tools_used
WHERE o_net_soc_code = '15-1252.00'  -- Software Developer
LIMIT 5;

-- Output:
-- Graphics processing unit GPU | Central processing unit CPU processors
-- Application servers | Computer server
-- Desktop computers | Desktop computer
-- Mainframe computers | Mainframe computer
```

**Use Cases:**
- Technology planning: "What tools/equipment do Software Developers need?"
- Market analysis: Track adoption of specific technologies by occupation
- Equipment budgeting: Identify all required tools for a role
- Career transition: Compare equipment/tools between roles
- Skill-to-tool mapping: "Which roles use Kubernetes?"

---

### 4. **task_ratings** (161,559 rows)

Detailed frequency ratings for tasks with **statistical confidence intervals**. Each task can have multiple rows (one per frequency category/scale).

**Schema:**
```sql
o_net_soc_code     TEXT    -- Occupation code
title              TEXT    -- Occupation title
task_id            INTEGER -- Unique task identifier
task               TEXT    -- Task description
scale_id           TEXT    -- "FT" (Frequency of Task)
scale_name         TEXT    -- "Frequency of Task (Categories 1-7)"
category           INTEGER -- Frequency category (1=Yearly or less, 7=Hourly or more)
data_value         REAL    -- Frequency percentage (0–100)
n                  INTEGER -- Sample size
standard_error     REAL    -- Statistical error
lower_ci_bound     REAL    -- 95% CI lower bound (%)
upper_ci_bound     REAL    -- 95% CI upper bound (%)
recommend_suppress TEXT    -- "Y" if suppress, else NULL
date               TEXT    -- Collection date
domain_source      TEXT    -- Data source (Incumbent, Occupational Expert, etc.)
```

**Frequency Categories (from task_categories table):**
| Category | Meaning |
|----------|---------|
| 1 | Yearly or less |
| 2 | More than yearly |
| 3 | More than monthly |
| 4 | More than weekly |
| 5 | Daily |
| 6 | Several times daily |
| 7 | Hourly or more |

**Example: Top-frequency tasks for Software Developer:**
```sql
SELECT task, category, data_value, lower_ci_bound, upper_ci_bound
FROM task_ratings
WHERE o_net_soc_code = '15-1252.00' AND category IS NOT NULL
ORDER BY data_value DESC
LIMIT 3;

-- Output:
-- Analyze information to... | 5 | 53.19 | 22.15 | 81.93
-- Confer with data processing... | 4 | 47.71 | 35.00 | 60.73
-- Modify existing software... | 4 | 47.04 | 24.34 | 71.03
```

*(Note: `category IS NOT NULL` filters out aggregate/relevance scores)*

**Use Cases:**
- **Time allocation**: "How much time do developers spend on coding vs. meetings?"
- **Statistical rigor**: Use confidence intervals to assess data reliability
- **Job analysis**: Identify tasks done daily vs. yearly
- **Workforce planning**: Prioritize training for high-frequency tasks
- **Research**: Reliable occupational task data with error bounds

---

### 5. **level_scale_anchors** (483 rows)

Interpretive examples for ability rating scales. Maps abstract ability levels to concrete behavioral examples.

**Schema:**
```sql
scale_id          TEXT    -- Scale identifier (e.g., "AB" for Abilities)
scale_name        TEXT    -- Scale name (e.g., "Abilities")
element_id        TEXT    -- Ability identifier
element_name      TEXT    -- Ability name (e.g., "Oral Comprehension")
level             INTEGER -- Rating level (1–7 typically)
description       TEXT    -- Concrete example/anchor
date              TEXT    -- Collection date
domain_source     TEXT    -- Data source
```

**Example: What does "Oral Comprehension Level 2" mean?**
```sql
SELECT element_name, level, description FROM level_scale_anchors
WHERE element_name = 'Oral Comprehension' AND level = 2;

-- Output:
-- Oral Comprehension | 2 | Understand a TV commercial
```

**Use Cases:**
- **Job descriptions**: Make ability requirements concrete and understandable
- **Assessment design**: Create test questions matching specific levels
- **Training**: Tailor instruction to target a specific ability level
- **Interviews**: Ask questions that probe specific ability anchors

---

### 6. **occupation_level_metadata** (32,202 rows)

Data quality and collection metadata per occupation. Shows which occupations have reliable data and which may be incomplete.

**Schema:**
```sql
o_net_soc_code              TEXT    -- Occupation code
title                       TEXT    -- Occupation title
data_collection_mode        TEXT    -- How data was collected (e.g., "O*NET Survey", "Job Analysis")
occupational_data_completeness REAL -- Completeness percentage (0–100)
survey_date                 TEXT    -- Data collection date
n_respondents               INTEGER -- Number of respondents
```

**Example:**
```sql
SELECT o_net_soc_code, title, occupational_data_completeness
FROM occupation_level_metadata
WHERE occupational_data_completeness < 50
LIMIT 3;

-- Output:
-- 11-0011.00 | Chief Executives | 45.2
-- 29-9999.00 | Other Occupations | 30.1
```

**Use Cases:**
- **Data quality**: Identify high-confidence vs. speculative occupational data
- **Research**: Filter for only complete occupation records
- **Analysis**: Weight conclusions by occupational data completeness
- **Coverage**: Determine which occupations have robust survey data

---

## Relationship Tables (Join Tables)

### 7. **skills_to_work_activities**

Links skills to work activities. **Usage:** Find which skills are used in which work activities.

```sql
SELECT DISTINCT s.element_name, wa.element_name
FROM skills_to_work_activities swf
JOIN skills s ON swf.skill_id = s.element_id
JOIN work_activities wa ON swf.activity_id = wa.element_id
WHERE swf.o_net_soc_code = '15-1252.00'
LIMIT 5;
```

### 8. **abilities_to_work_activities**

Links abilities to work activities. **Usage:** Find which abilities are needed for specific work activities.

```sql
SELECT DISTINCT a.element_name, wa.element_name
FROM abilities_to_work_activities aaf
JOIN abilities a ON aaf.ability_id = a.element_id
JOIN work_activities wa ON aaf.activity_id = wa.element_id
LIMIT 5;
```

### 9. **skills_to_work_context** & **abilities_to_work_context**

Map skills/abilities to work conditions/environments (similar pattern to above).

---

## Reference Tables

### 10–18. Reference Lookup Tables

These tables provide standardized category definitions:

- **task_categories** — Task frequency categories (1–7, with descriptions)
- **job_zone_reference** — Job Zone definitions and examples
- **scales_reference** — All available rating scales (Abilities, Skills, etc.)
- **dwa_reference** — Data-Wise Activities taxonomy
- **iwa_reference** — Integrated Work Activities taxonomy
- **unspsc_reference** — UNSPSC commodity codes for tools/equipment
- **content_model_reference** — O*NET content model structure
- **survey_booklet_locations** — Metadata on data collection booklets
- **_metadata** — Database version, build date, etc.

**Example: Look up O*NET database version:**
```sql
SELECT value FROM _metadata WHERE key = 'version';
-- Output: 30.2
```

---

## Quick SQL Query Recipes

### Recipe 1: Find all tasks a Software Developer does DAILY
```sql
SELECT task, data_value as frequency_pct, lower_ci_bound, upper_ci_bound
FROM task_ratings
WHERE o_net_soc_code = '15-1252.00' AND category = 5  -- 5 = Daily
ORDER BY data_value DESC;
```

### Recipe 2: Compare equipment use between two roles
```sql
SELECT t1.example, COUNT(DISTINCT t1.o_net_soc_code) as occupations
FROM tools_used t1
WHERE t1.example IN (
    SELECT example FROM tools_used 
    WHERE o_net_soc_code = '15-1252.00'  -- Software Developer tools
)
GROUP BY t1.example
ORDER BY occupations DESC;
```

### Recipe 3: Find occupations with emerging tasks in your field
```sql
SELECT DISTINCT o_net_soc_code, title, task
FROM emerging_tasks
WHERE title LIKE '%Manager%'
ORDER BY date DESC;
```

### Recipe 4: RIASEC profile for an occupation
```sql
SELECT element_name, data_value
FROM interests
WHERE o_net_soc_code = '15-1252.00'
  AND element_name NOT LIKE '%High-Point%'
ORDER BY data_value DESC;
```

### Recipe 5: Interpret an ability rating
```sql
SELECT element_name, level, description
FROM level_scale_anchors
WHERE element_name = 'Problem Sensitivity' AND level <= 4
ORDER BY level;
```

---

## Notes

- All queries should filter by `o_net_soc_code` to target specific occupations
- Use `LIMIT` to avoid returning excessive data (some tables have 160K+ rows)
- Confidence intervals (`lower_ci_bound`, `upper_ci_bound`) indicate statistical reliability
- `recommend_suppress = 'Y'` flags questionable/unreliable data points
- Most tables include a `date` field tracking when data was collected
- Use `PRAGMA table_info(table_name);` to inspect exact column names

---

## When to Use These Tables

| Scenario | Recommended Tables |
|----------|-------------------|
| Career counseling / personality matching | `interests` (RIASEC) |
| Identify new skills trending in an occupation | `emerging_tasks`, `tools_used` |
| Job analysis / create accurate job descriptions | `task_ratings`, `level_scale_anchors` |
| Equipment budgeting / tech planning | `tools_used` |
| Validate research findings | Use confidence intervals from `task_ratings` |
| Data quality / filter for reliable occupations | `occupation_level_metadata` |
| Understand relationships between skills and activities | `skills_to_work_activities`, `abilities_to_work_activities` |

