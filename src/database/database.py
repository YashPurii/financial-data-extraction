import sqlite3
import json
import os

# ---------------- Database Setup ----------------
DB_PATH = "C:/Users/yashp/OneDrive/Desktop/financial-data-extraction/data/financial_data.db"

def create_database():
    """Creates a SQLite database and tables for storing financial data."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS financial_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        content TEXT
    )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Database & Table Created Successfully!")

# ---------------- Insert Data ----------------
def insert_data(source, content):
    """Inserts extracted financial data into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO financial_data (source, content) VALUES (?, ?)", (source, content))
    
    conn.commit()
    conn.close()

# ---------------- Load and Store Data ----------------
def store_extracted_data():
    """Reads validated data and inserts it into the database."""
    validated_data_path = "C:/Users/yashp/OneDrive/Desktop/financial-data-extraction/data/processed/validated_data_validated.json"
    
    if not os.path.exists(validated_data_path):
        print("❌ Error: Validated data file not found.")
        return

    with open(validated_data_path, "r", encoding="utf-8") as file:
        validated_data = json.load(file)

    for source, content in validated_data.items():
        insert_data(source, content)
    
    print("✅ All Extracted Data Stored in Database!")

# ---------------- Retrieve Data ----------------
def fetch_data():
    """Retrieves and displays stored financial data."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM financial_data")
    rows = cursor.fetchall()

    conn.close()
    return rows

# ---------------- Main Execution ----------------
if __name__ == "__main__":
    create_database()
    store_extracted_data()
    
    print("\n📂 Retrieved Data from Database:")
    for row in fetch_data():
        print(row)
