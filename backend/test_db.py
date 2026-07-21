from app.database import SessionLocal
from sqlalchemy import text

db = SessionLocal()

try:
    result = db.execute(text("SELECT COUNT(*) FROM companies"))
    print("Total Companies:", result.scalar())

finally:
    db.close()