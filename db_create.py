import sqlite3


def create_db():
    with sqlite3.connect('hospital.db') as conn:
        cur = conn.cursor()

        cur.executescript('''CREATE TABLE IF NOT EXISTS patients
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    surname TEXT NOT NULL,
                    health TEXT NOT NULL,
                    disease TEXT NOT NULL);
    
                   CREATE TABLE IF NOT EXISTS users
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   login TEXT NOT NULL UNIQUE,
                   password TEXT NOT NULL UNIQUE,
                   admin_role INTEGER NOT NULL);
                   ''')
        conn.commit()
