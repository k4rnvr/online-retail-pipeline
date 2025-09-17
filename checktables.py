import psycopg2

try:
    conn = psycopg2.connect(
        dbname="retaildb",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    print("Connected to Postgres successfully!")
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    print(cur.fetchall())
    cur.close()
    conn.close()

except Exception as e:
    print("❌ Error:", e)
