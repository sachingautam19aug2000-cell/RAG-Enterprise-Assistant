
import sqlite3
import os

PROJECT_PATH = os.path.dirname(
    os.path.abspath(__file__)
)

DB_PATH = os.path.join(
    PROJECT_PATH,
    "rag_assistant.db"
)

connection = sqlite3.connect(DB_PATH)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS rag_query_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    question TEXT NOT NULL,
    answer TEXT,
    sources TEXT
)
""")

connection.commit()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
""")

print("Database created successfully.")
print("Tables:", cursor.fetchall())

connection.close()
