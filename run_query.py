import psycopg2
import sys
from decimal import Decimal

def run_query_from_file(file_path):
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="retaildb",
            user="postgres",
            password="postgres"
        )
        cur = conn.cursor()

        with open(file_path, "r") as f:
            query = f.read()

        cur.execute(query)
        colnames = [desc[0] for desc in cur.description]  
        results = cur.fetchall()

        print(" | ".join(colnames))
        print("-" * 50)
        for row in results:
            formatted = [
                str(item) if not isinstance(item, Decimal) else f"{item:,.2f}"
                for item in row
            ]
            print(" | ".join(formatted))

        cur.close()
        conn.close()
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_query.py <path_to_sql_file>")
    else:
        run_query_from_file(sys.argv[1])
