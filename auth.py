from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db

def register_user(username, email, password):
    db = get_db()
    hashed_password = generate_password_hash(password)
    try:
        db.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, hashed_password)
        )
        db.commit()
        return True
    except Exception as e:
        print(f"Registration error: {e}")
        return False
    finally:
        db.close()

def login_user(username, password):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    db.close()
    
    if user and check_password_hash(user['password_hash'], password):
        return user
    return None
