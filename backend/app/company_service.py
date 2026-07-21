from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Company


def get_all_companies():

    db: Session = SessionLocal()

    try:
        companies = db.query(Company).all()

        result = []

        for company in companies:

            result.append({
                "id": company.id,
                "company_name": company.company_name,
                "symbol": company.symbol,
                "sector": company.sector
            })

        return result

    finally:
        db.close()


def get_company(company_id: int):

    db: Session = SessionLocal()

    try:

        company = db.query(Company).filter(
            Company.id == company_id
        ).first()

        if company is None:

            return {
                "message": "Company not found"
            }

        return {
            "id": company.id,
            "company_name": company.company_name,
            "symbol": company.symbol,
            "sector": company.sector,
            "website": company.website,
            "about_company": company.about_company
        }

    finally:
        db.close()