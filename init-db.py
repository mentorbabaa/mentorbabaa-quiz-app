import sqlite3

conn = sqlite3.connect('app.db')  # or whatever your path is
with open('schema_dev.sql', 'r') as f:
    conn.executescript(f.read())
print("✅ SQLite tables created successfully.")
conn.close()
