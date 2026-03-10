# O*NET Data Dictionary

This document serves as a comprehensive reference for the 40 `.xlsx` files that comprise the O*NET Database. It describes the schema, relationships, and semantic meaning of the data to facilitate deep exploration and analysis.

## SQLite Table Mapping

All data is also available in `onet.db` (built by `scripts/onet_build_db.py`). Table and column names are snake_cased versions of the xlsx originals. Query `_file_map` for the full mapping, or use the table below:

| xlsx File | SQLite Table |
|-----------|-------------|
| Occupation Data.xlsx | `occupation_data` |
| Abilities.xlsx | `abilities` |
| Knowledge.xlsx | `knowledge` |
| Skills.xlsx | `skills` |
| Work Activities.xlsx | `work_activities` |
| Work Context.xlsx | `work_context` |
| Technology Skills.xlsx | `technology_skills` |
| Task Statements.xlsx | `task_statements` |
| Task Ratings.xlsx | `task_ratings` |
| Related Occupations.xlsx | `related_occupations` |
| Alternate Titles.xlsx | `alternate_titles` |
| Job Zones.xlsx | `job_zones` |
| Job Zone Reference.xlsx | `job_zone_reference` |
| Interests.xlsx | `interests` |
| Work Styles.xlsx | `work_styles` |
| Work Values.xlsx | `work_values` |
| Education, Training, and Experience.xlsx | `education_training_and_experience` |
| Education, Training, and Experience Categories.xlsx | `education_training_and_experience_categories` |
| Content Model Reference.xlsx | `content_model_reference` |
| Scales Reference.xlsx | `scales_reference` |

Column name mapping: `O*NET-SOC Code` -> `o_net_soc_code`, `Element ID` -> `element_id`, `Data Value` -> `data_value`, etc.

FTS5 virtual tables: `occupation_fts` (titles + descriptions), `alternate_titles_fts` (alternate job titles).

## Relationships Diagram

The O*NET database is built on a central "Content Model" that links worker characteristics and requirements to occupational requirements.

```text
[Occupation Data] <--- (O*NET-SOC Code) ---> [Abilities/Knowledge/Skills/Interests]
       |                                              |
       |                                       (Element ID)
       |                                              |
       |                                   [Content Model Reference]
       |                                              |
       |                                       (Element ID)
       |                                              |
(O*NET-SOC Code)                      [Work Activities/Work Context]
       |                                              |
       + <--- (Task ID) ---> [Task Statements] <--- (DWA ID) ---> [DWA Reference]
       |                                              |
       + <--- (Commodity Code) ---> [Technology Skills / Tools Used]
```

## Schema Patterns

### The Standard Rated Schema (15 Columns)
Many files (Abilities, Knowledge, Skills, Work Activities) use a consistent 15-column format to store ratings. This allows for a standardized way to compare different domains.

| Column | Data Type | Description |
| :--- | :--- | :--- |
| O*NET-SOC Code | String | Primary identifier for the occupation |
| Title | String | Occupational title |
| Element ID | String | Identifier for the Content Model element |
| Element Name | String | Name of the specific characteristic (e.g., Oral Comprehension) |
| Scale ID | String | Identifier for the rating scale (IM for Importance, LV for Level) |
| Scale Name | String | Human-readable name of the scale |
| Data Value | Float | The actual rating (mean or percentage) |
| N | Integer | Sample size (number of respondents) |
| Standard Error | Float | Indication of data precision |
| Lower CI Bound | Float | 95% confidence interval lower limit |
| Upper CI Bound | Float | 95% confidence interval upper limit |
| Recommend Suppress | String | "Y" if data should be used with caution |
| Not Relevant | String | "Y" if the element is not relevant to the occupation (context only) |
| Date | Date | When the data was last updated |
| Domain Source | String | Source of data (e.g., Analyst, Incumbent) |

## Scale Reference

| Scale ID | Scale Name | Min | Max | Usage |
| :--- | :--- | :--- | :--- | :--- |
| IM | Importance | 1 | 5 | How important the skill/ability is to the job |
| LV | Level | 0 | 7 | The degree of complexity or expertise required |
| OI | Occupational Interests | 1 | 7 | Interest scores for RIASEC types |
| DR | Distinctiveness Rank | 1 | 16 | Ranking for work styles |
| EX | Extent | 1 | 7 | Extent of a work value |

## Element ID Hierarchy

Element IDs follow a hierarchical structure that allows for aggregation at different levels:
- **Level 1 (e.g., 1.A)**: Broad domain (e.g., Worker Characteristics)
- **Level 2 (e.g., 1.A.1)**: Major category (e.g., Cognitive Abilities)
- **Level 3 (e.g., 1.A.1.a)**: Sub-category (e.g., Verbal Abilities)
- **Level 4 (e.g., 1.A.1.a.1)**: Specific element (e.g., Oral Comprehension)

---

## Group: Core Occupation

### Occupation Data.xlsx
- **Purpose**: The master list of all occupations in the O*NET-SOC taxonomy.
- **Columns**: O*NET-SOC Code (String), Title (String), Description (String).
- **Relationships**: Links to almost every other file via O*NET-SOC Code.
- **Sample**: `11-1011.00 | Chief Executives | Determine and formulate policies...`
- **Row Count**: 1,016

---

## Group: Worker Characteristics

### Abilities.xlsx
- **Purpose**: Ratings of enduring attributes of the individual that influence performance.
- **Columns**: 15-column rated schema.
- **Relationships**: Links to `Occupation Data` (O*NET-SOC Code) and `Content Model Reference` (Element ID).
- **Sample**: `11-1011.00 | Chief Executives | 1.A.1.a.1 | Oral Comprehension | IM | Importance | 4.62`
- **Row Count**: 92,976

### Interests.xlsx
- **Purpose**: Holland RIASEC (Realistic, Investigative, Artistic, Social, Enterprising, Conventional) scores.
- **Columns**: O*NET-SOC Code, Title, Element ID, Element Name, Scale ID (OI), Scale Name, Data Value, Date, Domain Source.
- **Relationships**: Links to `Occupation Data` and `RIASEC Keywords`.
- **Sample**: `11-1011.00 | Chief Executives | 1.B.1.a | Realistic | OI | Occupational Interests | 1.26`
- **Row Count**: 8,307

### Work Styles.xlsx
- **Purpose**: Personal characteristics that can affect how well someone performs a job.
- **Columns**: O*NET-SOC Code, Title, Element ID, Element Name, Scale ID (DR), Scale Name, Data Value, Date, Domain Source.
- **Sample**: `11-1011.00 | Chief Executives | 1.D.1.a | Innovation | DR | Distinctiveness Rank | 7`
- **Row Count**: 37,422

### Work Values.xlsx
- **Purpose**: Global aspects of work that are important to a person's satisfaction.
- **Columns**: O*NET-SOC Code, Title, Element ID, Element Name, Scale ID (EX), Scale Name, Data Value, Date, Domain Source.
- **Sample**: `11-1011.00 | Chief Executives | 1.B.2.a | Achievement | EX | Extent | 6.33`
- **Row Count**: 7,866

---

## Group: Worker Requirements

### Knowledge.xlsx
- **Purpose**: Organized sets of principles and facts applied in general domains.
- **Columns**: 15-column rated schema.
- **Row Count**: 59,004

### Skills.xlsx
- **Purpose**: Developed capacities that facilitate learning or the more rapid acquisition of knowledge.
- **Columns**: 15-column rated schema.
- **Row Count**: 62,580

---

## Group: Experience Requirements

### Education, Training, and Experience.xlsx
- **Purpose**: Typical education, training, and experience requirements for occupations.
- **Columns**: O*NET-SOC Code, Title, Element ID, Element Name, Scale ID, Scale Name, Category (Numeric), Data Value, N, Standard Error, Lower CI Bound, Upper CI Bound, Recommend Suppress, Date, Domain Source.
- **Relationships**: Category maps to `Education, Training, and Experience Categories`.
- **Row Count**: 37,125

### Education, Training, and Experience Categories.xlsx
- **Purpose**: Metadata explaining what the numeric categories in the above file mean.
- **Columns**: Element ID, Element Name, Scale ID, Scale Name, Category, Category Description.
- **Sample**: `2.D.1 | Required Level of Education | RL | Category 1 | Less than a High School Diploma`
- **Row Count**: 41

### Job Zones.xlsx
- **Purpose**: Classification of occupations into one of five categories based on required education and training.
- **Columns**: O*NET-SOC Code, Title, Job Zone (1-5), Date, Domain Source.
- **Relationships**: Links to `Job Zone Reference`.
- **Row Count**: 923

### Job Zone Reference.xlsx
- **Purpose**: Detailed description of what each Job Zone level implies.
- **Columns**: Job Zone, Name, Experience, Education, Job Training, Examples, SVP Range.
- **Row Count**: 4

---

## Group: Occupational Requirements

### Work Activities.xlsx
- **Purpose**: General types of job behaviors occurring across multiple occupations.
- **Columns**: 15-column rated schema.
- **Row Count**: 73,308

### Work Context.xlsx
- **Purpose**: Physical and social factors that influence the nature of work.
- **Columns**: 16 columns (Adds 'Category' and 'Not Relevant' to the standard rated schema).
- **Relationships**: Category maps to `Work Context Categories`.
- **Row Count**: 297,676

### Task Statements.xlsx
- **Purpose**: Occupation-specific tasks performed.
- **Columns**: O*NET-SOC Code, Title, Task ID, Task, Task Type, Incumbents Responding, Date, Domain Source.
- **Relationships**: Task ID links to `Task Ratings` and `Tasks to DWAs`.
- **Row Count**: 18,796

### Task Ratings.xlsx
- **Purpose**: Importance and Frequency ratings for specific tasks.
- **Columns**: O*NET-SOC Code, Title, Task ID, Task, Scale ID, Scale Name, Category, Data Value, N, Standard Error, Lower CI Bound, Upper CI Bound, Recommend Suppress, Date, Domain Source.
- **Row Count**: 161,559

---

## Group: Occupation-Specific Information

### Technology Skills.xlsx
- **Purpose**: Software and technical skills required for an occupation.
- **Columns**: O*NET-SOC Code, Title, Example, Commodity Code, Commodity Title, Hot Technology, In Demand.
- **Relationships**: Commodity Code links to `UNSPSC Reference`.
- **Sample**: `11-1011.00 | Chief Executives | Adobe Acrobat | 43232202 | Document management software | Y | N`
- **Row Count**: 32,773

### Tools Used.xlsx
- **Purpose**: Physical tools and equipment used.
- **Columns**: O*NET-SOC Code, Title, Example, Commodity Code, Commodity Title.
- **Relationships**: Commodity Code links to `UNSPSC Reference`.
- **Row Count**: 41,662

### Emerging Tasks.xlsx
- **Purpose**: Identification of new or significantly changed tasks.
- **Columns**: O*NET-SOC Code, Title, Task, Category (New/Changed), Original Task ID, Original Task, Date, Domain Source.
- **Row Count**: 328

### Alternate Titles.xlsx
- **Purpose**: Other names used by employers for a given occupation.
- **Columns**: O*NET-SOC Code, Title, Alternate Title, Short Title, Source(s).
- **Row Count**: 57,543

### Sample of Reported Titles.xlsx
- **Purpose**: Real-world job titles reported by workers.
- **Columns**: O*NET-SOC Code, Title, Reported Job Title, Shown in My Next Move.
- **Row Count**: 7,953

### Related Occupations.xlsx
- **Purpose**: Cross-walk between occupations with similar profiles.
- **Columns**: O*NET-SOC Code, Title, Related O*NET-SOC Code, Related Title, Relatedness Tier, Index.
- **Row Count**: 18,460

---

## Group: Reference & Taxonomy

### Content Model Reference.xlsx
- **Purpose**: The master taxonomy defining all Element IDs and their descriptions.
- **Columns**: Element ID, Element Name, Description.
- **Row Count**: 630

### Scales Reference.xlsx
- **Purpose**: Definitions of all rating scales used in the database.
- **Columns**: Scale ID, Scale Name, Minimum, Maximum.
- **Row Count**: 31

### Level Scale Anchors.xlsx
- **Purpose**: Examples of what specific scores mean on a Level (LV) scale.
- **Columns**: Element ID, Element Name, Scale ID, Scale Name, Anchor Value, Anchor Description.
- **Row Count**: 483

### UNSPSC Reference.xlsx
- **Purpose**: Mapping of Commodity Codes to the United Nations Standard Products and Services Code.
- **Columns**: Commodity Code, Commodity Title, Class Code, Class Title, Family Code, Family Title, Segment Code, Segment Title.
- **Row Count**: 4,264

### IWA Reference.xlsx
- **Purpose**: Intermediate Work Activities (higher-level grouping than DWAs).
- **Columns**: Element ID, Element Name, IWA ID, IWA Title.
- **Row Count**: 332

### DWA Reference.xlsx
- **Purpose**: Detailed Work Activities that group tasks into manageable behaviors.
- **Columns**: Element ID, Element Name, IWA ID, IWA Title, DWA ID, DWA Title.
- **Row Count**: 2,087

### Tasks to DWAs.xlsx
- **Purpose**: Mapping of individual occupation-specific tasks to universal Detailed Work Activities.
- **Columns**: O*NET-SOC Code, Title, Task ID, Task, DWA ID, DWA Title, Date, Domain Source.
- **Row Count**: 23,850

### Task Categories.xlsx
- **Purpose**: Definitions for categories used in task ratings (e.g., Frequency).
- **Columns**: Scale ID, Scale Name, Category, Category Description.
- **Row Count**: 7

### Work Context Categories.xlsx
- **Purpose**: Definitions for categories used in Work Context ratings.
- **Columns**: Element ID, Element Name, Scale ID, Scale Name, Category, Category Description.
- **Row Count**: 281

---

## Group: Interest Reference

### RIASEC Keywords.xlsx
- **Purpose**: Keywords that describe the essence of Holland interest types.
- **Columns**: Element ID, Element Name, Keyword, Keyword Type (Action/Object).
- **Row Count**: 75

### Basic Interests to RIASEC.xlsx
- **Purpose**: High-level mapping of basic interests to the RIASEC domains.
- **Columns**: Basic Interests Element ID, Basic Interests Element Name, RIASEC Element ID, RIASEC Element Name.
- **Row Count**: 53

### Interests Illustrative Activities.xlsx
- **Purpose**: Examples of activities that appeal to specific interest types.
- **Columns**: Element ID, Element Name, Interest Type, Activity.
- **Row Count**: 188

### Interests Illustrative Occupations.xlsx
- **Purpose**: Example occupations that align with specific interest types.
- **Columns**: Element ID, Element Name, Interest Type, O*NET-SOC Code, Title.
- **Row Count**: 186

---

## Group: Cross-Domain Linkage

### Abilities to Work Activities.xlsx
- **Purpose**: Direct links between worker abilities and general work activities.
- **Columns**: Abilities Element ID, Abilities Element Name, Work Activities Element ID, Work Activities Element Name.
- **Row Count**: 381

### Abilities to Work Context.xlsx
- **Purpose**: Direct links between worker abilities and the work environment context.
- **Row Count**: 139

### Skills to Work Activities.xlsx
- **Purpose**: Direct links between worker skills and general work activities.
- **Row Count**: 232

### Skills to Work Context.xlsx
- **Purpose**: Direct links between worker skills and the work environment context.
- **Row Count**: 96

---

## Group: Data Collection Metadata

### Occupation Level Metadata.xlsx
- **Purpose**: Technical details on survey response rates and methodology per occupation.
- **Columns**: O*NET-SOC Code, Title, Item, Response, N, Percent, Date.
- **Row Count**: 32,202

### Survey Booklet Locations.xlsx
- **Purpose**: Mapping of Content Model elements to the actual survey questions.
- **Columns**: Element ID, Element Name, Survey Item Number, Scale ID, Scale Name.
- **Row Count**: 211
