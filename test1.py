import os

base_dir = os.path.dirname(os.path.abspath(__file__))
sql_path = os.path.join(base_dir, "..", "queries", "distinct_countries.sql")
print("Looking for SQL file at:", os.path.abspath(sql_path))
print("Exists?", os.path.exists(sql_path))
print("Files in folder:", os.listdir(os.path.join(base_dir, "..", "queries")))

#/Users/karanveersingh/online_retail_pipeline/queries/distinct_countries.sql