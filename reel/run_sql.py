
import sqlite3

database_path = "data/reel_insights.db"
sql_file = "sql/10_top_rated_movies.sql"
connection = sqlite3.connect(database_path)

try:
    with open(sql_file, "r", encoding="utf-8") as file:
        query = file.read()

    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    print("Top 10 Highest-Rated Movies")
    print("-" * 40)

    for row in results:
        print(row)

finally:
    connection.close()
