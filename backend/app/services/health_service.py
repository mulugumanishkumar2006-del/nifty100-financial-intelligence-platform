"""
Company Health Score Service

NIFTY100 Financial Intelligence Platform
"""

import sqlite3
from pathlib import Path


# ==========================================================
# Database
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATABASE = PROJECT_ROOT / "database" / "nifty100.db"


def get_connection():

    return sqlite3.connect(DATABASE)



# ==========================================================
# Company Health Score
# ==========================================================

def calculate_health_score(company_id: str):

    connection = get_connection()


    # Fetch company financial metrics

    query = """
    SELECT

        roe_percentage,
        roce_percentage,
        book_value,
        face_value

    FROM companies

    WHERE id = ?

    """


    cursor = connection.execute(
        query,
        (company_id,)
    )


    data = cursor.fetchone()


    connection.close()



    if data is None:

        return None



    roe = data[0] or 0

    roce = data[1] or 0

    book_value = data[2] or 0

    face_value = data[3] or 0



    # ======================================================
    # Scoring Logic
    # ======================================================


    profitability_score = min(
        max(roe * 4, 0),
        100
    )


    efficiency_score = min(
        max(roce * 4, 0),
        100
    )


    growth_score = min(
        max(book_value / 10, 0),
        100
    )


    risk_score = 80



    final_score = round(
        (
            profitability_score
            +
            efficiency_score
            +
            growth_score
            +
            risk_score

        ) / 4
    )



    if final_score >= 80:

        rating = "Strong"


    elif final_score >= 60:

        rating = "Moderate"


    else:

        rating = "Weak"



    return {

        "company_id": company_id,

        "health_score": final_score,

        "rating": rating,


        "factors": {

            "profitability":
                round(profitability_score,2),


            "efficiency":
                round(efficiency_score,2),


            "growth":
                round(growth_score,2),


            "risk":
                risk_score

        }

    }