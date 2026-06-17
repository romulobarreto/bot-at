from src.db.connection import get_connection

conn = get_connection()

cursor = conn.cursor()

cursor.execute("""
SELECT DISTINCT INSTALACAO
FROM equipamentos
WHERE INSTALACAO = '62670662'
""")

rows = cursor.fetchall()

print(rows)