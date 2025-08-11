import pyodbc
import pandas as pd
import os

mdb_file = r"C:\Users\hugo\OneDrive\Documents\ALL Engineering\Machine-Learning\GenAI Projects\Aerospace Incident Report Analyzer\avall.mdb"
output_dir = "converted_csvs"
os.makedirs(output_dir, exist_ok=True)

# Set up connection string
conn_str = (
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
    rf"DBQ={mdb_file};"
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# List all tables
tables = [row.table_name for row in cursor.tables(tableType='TABLE')]
print("Available Tables:\n", tables)

# Export selected tables
target_tables = ["events", "narratives", "Findings", "aircraft"]
for table in target_tables:
    print(f"Exporting: {table}")
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    df.to_csv(os.path.join(output_dir, f"{table}.csv"), index=False)

conn.close()
print("✅ Done! CSVs are in the converted_csvs folder.")
