import sqlite3

conn = sqlite3.connect("../database/nifty100.db")

cursor = conn.cursor()

cursor.execute("""
SELECT DISTINCT company_id
FROM profitandloss
LIMIT 20
""")

rows = cursor.fetchall()

print("Company IDs:")
for row in rows:
    print(row[0])

conn.close()