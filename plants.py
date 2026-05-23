from database import get_db
from datetime import datetime

def add_plant(user_id, name, species, location, watering_interval_days, notes):
    db = get_db()
    db.execute(
        "INSERT INTO plants (user_id, name, species, location, watering_interval_days, notes) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, name, species, location, watering_interval_days, notes)
    )
    db.commit()
    db.close()

def get_all_plants(user_id):
    db = get_db()
    plants = db.execute("SELECT * FROM plants WHERE user_id = ?", (user_id,)).fetchall()
    db.close()
    return plants

def get_plant_details(plant_id, user_id):
    db = get_db()
    plant = db.execute("SELECT * FROM plants WHERE id = ? AND user_id = ?", (plant_id, user_id)).fetchone()
    db.close()
    return plant

def update_plant(plant_id, user_id, name, species, location, watering_interval_days, notes):
    db = get_db()
    db.execute(
        "UPDATE plants SET name=?, species=?, location=?, watering_interval_days=?, notes=? WHERE id=? AND user_id=?",
        (name, species, location, watering_interval_days, notes, plant_id, user_id)
    )
    db.commit()
    db.close()

def delete_plant(plant_id, user_id):
    db = get_db()
    db.execute("DELETE FROM plants WHERE id = ? AND user_id = ?", (plant_id, user_id))
    db.commit()
    db.close()

def log_watering(plant_id, note):
    db = get_db()
    today = datetime.now().strftime('%Y-%m-%d')
    db.execute("INSERT INTO watering_logs (plant_id, note) VALUES (?, ?)", (plant_id, note))
    db.execute("UPDATE plants SET last_watered = ? WHERE id = ?", (today, plant_id))
    db.commit()
    db.close()

def get_watering_history(plant_id):
    db = get_db()
    logs = db.execute("SELECT * FROM watering_logs WHERE plant_id = ? ORDER BY watered_at DESC", (plant_id,)).fetchall()
    db.close()
    return logs
