import pandas as pd

df = pd.read_csv("staging/fact_sales.csv")
print(df.columns.tolist())
