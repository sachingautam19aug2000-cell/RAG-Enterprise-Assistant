import psycopg2

try:
    connection = psycopg2.connect(
        host="localhost",
        database="rag_enterprise_assistant",
        user="postgres",
        password="Sachin@10",
        port="5432"
    )

    print("PostgreSQL connection successful!")

    connection.close()

except Exception as error:
    print("Connection failed:")
    print(error)


import os
import json
import psycopg2


PROJECT_PATH = os.path.dirname(
    os.path.abspath(__file__)
)

LOG_FILE = os.path.join(
    PROJECT_PATH,
    "query_logs.json"
)


# PostgreSQL connection
connection = psycopg2.connect(
    host="localhost",
    database="rag_enterprise_assistant",
    user="postgres",
    password="YOUR_POSTGRES_PASSWORD",
    port="5432"
)

cursor = connection.cursor()


# Read JSON file
with open(
    LOG_FILE,
    "r",
    encoding="utf-8"
) as file:

    logs = json.load(file)


# Insert logs
for log in logs:

    cursor.execute(
        """
        INSERT INTO rag_query_logs
        (timestamp, question, answer, sources)
        VALUES (%s, %s, %s, %s)
        """,
        (
            log["timestamp"],
            log["question"],
            log["answer"],
            ", ".join(log["sources"])
        )
    )


connection.commit()

cursor.close()
connection.close()


print("All query logs inserted into PostgreSQL successfully.")
print("Total records:", len(logs))
