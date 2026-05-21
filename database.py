import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'plant_care.db')

def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(app):
    db = get_db()
    try:
        with open(os.path.join(BASE_DIR, 'schema.sql'), 'r') as f:
            db.executescript(f.read())
        db.commit()
        print(f"Database successfully initialized at: {DATABASE_PATH}")
    except Exception as e:
        print(f"Database initialization error: {e}")
    finally:
        db.close()
