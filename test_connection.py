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
    cur.execute("SELECT version();")
    print("Postgres version:", cur.fetchone())

    cur.close()
    conn.close()

except Exception as e:
    print("❌ Error:", e)


import psycopg2

conn = psycopg2.connect(
    dbname="retaildb",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Example: Create dim_customer
cur.execute("""
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id INT PRIMARY KEY,
    country VARCHAR(100)
);
""")

conn.commit()
print("✅ Table created successfully!")

cur.close()
conn.close()

