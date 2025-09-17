import psycopg2
import csv

# --- Connection ---
conn = psycopg2.connect(
    dbname="retaildb",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# --- dim_customer ---
cur.execute("""
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id INT PRIMARY KEY,
    country VARCHAR(100)
);
""")
with open("staging/dim_customer.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        cur.execute(
            "INSERT INTO dim_customer (customer_id, country) VALUES (%s, %s) ON CONFLICT (customer_id) DO NOTHING;",
            (row[0], row[1])
        )
conn.commit()
print("✅ dim_customer loaded")

# --- dim_product ---
cur.execute("""
CREATE TABLE IF NOT EXISTS dim_product (
    stockcode VARCHAR(50) PRIMARY KEY,
    description TEXT
);
""")
with open("staging/dim_product.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        cur.execute(
            "INSERT INTO dim_product (stockcode, description) VALUES (%s, %s) ON CONFLICT (stockcode) DO NOTHING;",
            (row[0], row[1])
        )
conn.commit()
print("✅ dim_product loaded")

# --- dim_date ---
cur.execute("""
CREATE TABLE IF NOT EXISTS dim_date (
    date_id DATE PRIMARY KEY,
    year INT,
    month INT,
    day INT,
    weekday INT
);
""")
with open("staging/dim_date.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        cur.execute(
            "INSERT INTO dim_date (date_id, year, month, day, weekday) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (date_id) DO NOTHING;",
            (row[0], row[1], row[2], row[3], row[4])
        )
conn.commit()
print("✅ dim_date loaded")

# --- fact_sales ---
# --- fact_sales ---
cur.execute("""
CREATE TABLE IF NOT EXISTS fact_sales (
    invoice VARCHAR(20),
    stockcode VARCHAR(50),
    quantity INT,
    invoicedate TIMESTAMP,
    price NUMERIC(10,2),
    customer_id INT,
    total_amount NUMERIC(12,2),
    is_cancelled BOOLEAN,
    is_return BOOLEAN,
    is_free BOOLEAN,
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (stockcode) REFERENCES dim_product(stockcode)
);
""")

with open("staging/fact_sales.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        invoice = row["Invoice"]
        stockcode = row["StockCode"]
        quantity = int(float(row["Quantity"])) if row["Quantity"] else 0
        invoicedate = row["InvoiceDate"]
        price = float(row["Price"]) if row["Price"] else 0.0

        cust_id = int(float(row["Customer ID"])) if row["Customer ID"] else None
        total_amount = float(row["TotalAmount"]) if row["TotalAmount"] else 0.0
        is_cancelled = (row["is_cancelled"].lower() == "true") if row["is_cancelled"] else False
        is_return = (row["is_return"].lower() == "true") if row["is_return"] else False
        is_free = (row["is_free"].lower() == "true") if row["is_free"] else False

        cur.execute(
            """INSERT INTO fact_sales
            (invoice, stockcode, quantity, invoicedate, price, customer_id, total_amount, is_cancelled)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
            (invoice, stockcode, quantity, invoicedate, price, cust_id, total_amount, is_cancelled)
        )

conn.commit()
print("✅ fact_sales loaded")


# --- Close ---
cur.close()
conn.close()
print("🎉 All tables created and loaded successfully")
