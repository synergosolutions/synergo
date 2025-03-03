"""
Database Wipe Script.
Dangerous-ish!
"""
import sqlite3

# Connect to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# List of tables to clear
tables = ['list', 'mail', 'new', 'texts', 'users']

# Delete all rows from each table
for table in tables:
    cursor.execute(f"DELETE FROM {table}")
    print(f"Cleared all rows from {table}")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("All specified tables have been cleared!")