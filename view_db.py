import sqlite3
import os

def view_database():
    db_path = 'instance/skill_exchange.db'
    if not os.path.exists(db_path):
        print(f"Database file not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table_name in tables:
        table_name = table_name[0]
        if table_name == 'sqlite_sequence':
            continue
            
        print(f"\n--- Table: {table_name} ---")
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [info[1] for info in cursor.fetchall()]
        print(" | ".join(columns))
        print("-" * (len(" | ".join(columns))))

        # Get rows
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        for row in rows:
            print(" | ".join(map(str, row)))

    conn.close()

if __name__ == "__main__":
    view_database()
