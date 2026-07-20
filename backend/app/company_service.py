from sqlalchemy import text
from app.database import SessionLocal


def get_all_companies():
    db = SessionLocal()

    try:

        query = text("""
            SELECT *
            FROM companies
            LIMIT 100
        """)

        result = db.execute(query)

        rows = result.fetchall()

        columns = result.keys()

        return [
            dict(zip(columns, row))
            for row in rows
        ]

    finally:
        db.close()


def get_company(company_id: int):

    db = SessionLocal()

    try:

        query = text("""
            SELECT *
            FROM companies
            WHERE id=:id
        """)

        result = db.execute(
            query,
            {"id": company_id}
        )

        row = result.fetchone()

        if row is None:
            return {}

        return dict(zip(result.keys(), row))

    finally:
        db.close()