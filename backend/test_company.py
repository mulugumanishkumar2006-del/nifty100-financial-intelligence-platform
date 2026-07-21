from sqlalchemy import text
from app.database import SessionLocal

db = SessionLocal()

try:
    query = text("""
        SELECT *
        FROM companies
        LIMIT 5
    """)

    result = db.execute(query)

    rows = result.fetchall()
    columns = result.keys()

    companies = [
        dict(zip(columns, row))
        for row in rows
    ]

    print(companies)

finally:
    db.close()