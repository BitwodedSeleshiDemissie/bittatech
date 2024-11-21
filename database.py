import sqlite3

def init_db():
    conn = sqlite3.connect('contacts.db')  # Connect to SQLite database (it will create it if it doesn't exist)
    c = conn.cursor()

    # Create a table for storing contact form data
    c.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
