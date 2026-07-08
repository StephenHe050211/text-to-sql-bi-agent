
import sqlite3
import sys
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "bi_agent_demo.db"

SAFE_QUERIES = {
    "monthly rebate by ae": """
        SELECT ae_id, ROUND(SUM(ae_rebate_hkd), 2) AS total_rebate_hkd
        FROM monthly_rebate
        GROUP BY ae_id
        ORDER BY total_rebate_hkd DESC;
    """,
    "top skills by salary": """
        SELECT skill, ROUND(AVG(salary_max), 0) AS avg_max_salary
        FROM job_skill_salary
        GROUP BY skill
        ORDER BY avg_max_salary DESC
        LIMIT 10;
    """,
}


def setup_demo_db(conn):
    monthly_rebate = pd.DataFrame([
        {"ae_id": "AE01", "market": "HKFE", "ae_rebate_hkd": 51.30},
        {"ae_id": "AE01", "market": "CME", "ae_rebate_hkd": 23.40},
        {"ae_id": "AE02", "market": "CME", "ae_rebate_hkd": 28.08},
    ])
    job_skill_salary = pd.DataFrame([
        {"skill": "SQL", "salary_max": 85000},
        {"skill": "Python", "salary_max": 95000},
        {"skill": "Power BI", "salary_max": 85000},
        {"skill": "RAG", "salary_max": 95000},
    ])
    monthly_rebate.to_sql("monthly_rebate", conn, if_exists="replace", index=False)
    job_skill_salary.to_sql("job_skill_salary", conn, if_exists="replace", index=False)


def validate_sql(sql):
    forbidden = ["drop", "delete", "update", "insert", "alter", "truncate"]
    lower_sql = sql.lower()
    if any(word in lower_sql for word in forbidden):
        raise ValueError("Unsafe SQL detected.")
    if not lower_sql.strip().startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")


def route_question(question):
    q = question.lower().strip()
    for key, sql in SAFE_QUERIES.items():
        if key in q:
            return sql
    raise ValueError("No approved query template matched the question. Add a reviewed template before execution.")


def main():
    question = " ".join(sys.argv[1:]) or "monthly rebate by AE"
    conn = sqlite3.connect(DB_PATH)
    try:
        setup_demo_db(conn)
        sql = route_question(question)
        validate_sql(sql)
        result = pd.read_sql_query(sql, conn)
        print("Question:", question)
        print("\nSQL executed:\n", sql.strip())
        print("\nResult:")
        print(result)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
