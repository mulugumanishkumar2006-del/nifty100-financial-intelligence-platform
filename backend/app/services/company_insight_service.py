"""
Company Insight Service
"""

def get_health_score(company_id: str):
    return {
        "company_id": company_id,
        "health_score": 75,
        "grade": "B"
    }


def get_recommendation(company_id: str):
    return {
        "company_id": company_id,
        "recommendation": "HOLD",
        "reason": "Default recommendation"
    }


def get_ai_summary(company_id: str):
    return {
        "company_id": company_id,
        "summary": "AI summary is under development.",
        "risk": "Medium"
    }


def get_company_insights(company_id: str):
    return {
        "health": get_health_score(company_id),
        "recommendation": get_recommendation(company_id),
        "summary": get_ai_summary(company_id),
    }