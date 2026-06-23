import sqlite3

DB_NAME = "notebook.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            activity TEXT NOT NULL,
            date TEXT NOT NULL,
            image_path TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            accesses INTEGER DEFAULT 0,
            records INTEGER DEFAULT 0
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM statistics")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO statistics (accesses, records) VALUES (0, 0)")
        
    conn.commit()
    conn.close()

def increment_access():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE statistics SET accesses = accesses + 1 WHERE id = 1")
    conn.commit()
    conn.close()

def update_record_count():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM activities")
    count = cursor.fetchone()[0]
    cursor.execute("UPDATE statistics SET records = ? WHERE id = 1", (count,))
    conn.commit()
    conn.close()