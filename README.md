# Text-to-SQL BI Agent

## One-line summary
A schema-aware BI assistant prototype that converts business questions into safe SQL queries and executes them on a sample analytics database.

## Why this project matters
Companies want business users to ask questions in plain English, but SQL agents must be safe: they should understand schema, avoid destructive queries, and explain the query result.

## Skills demonstrated
- Database schema design
- Natural-language-to-SQL mapping
- Query validation and guardrails
- BI-style answer generation

## How to run

```bash
python src/bi_agent.py "monthly rebate by AE"
python src/bi_agent.py "top skills by salary"
```

## Suggested resume bullet
Built a schema-aware Text-to-SQL BI agent with query guardrails, safe SQL execution, and business-friendly result summaries for analytics use cases.
