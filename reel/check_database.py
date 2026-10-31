
import sqlite3

database_path = "data/reel_insights.db"

connection = sqlite3.connect(database_path)

try:
    cursor = connection.cursor()

    print("Tables in your database:")
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
    """)

    tables = [row[0] for row in cursor.fetchall()]

    for table in tables:
        print(table)

    print("\nChecking number of rows in each table:")

    for table in tables:
        cursor.execute(f'SELECT COUNT(*) FROM "{table}"')
        row_count = cursor.fetchone()[0]
        print(f"{table}: {row_count} rows")

finally:
    connection.close()
