from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import init_db
from auth import register_user, login_user
from plants import add_plant, get_all_plants, get_plant_details, update_plant, delete_plant, log_watering, get_watering_history
from utils import days_until_watering, get_watering_status_label
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'super-secret-key-for-plant-care'

# Access Control Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please sign in to access this page.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if register_user(username, email, password):
            flash("Registration successful! You can now sign in.", "success")
            return redirect(url_for('login'))
        else:
            flash("Registration failed. Username or email might already be taken.", "danger")
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = login_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f"Welcome back, {user['username']}!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials. Please try again.", "danger")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Successfully signed out.", "info")
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_plants = get_all_plants(session['user_id'])
    processed_plants = []
    urgent_plants = []
    
    for plant in user_plants:
        plant_dict = dict(plant)
        days = days_until_watering(plant['last_watered'], plant['watering_interval_days'])
        label, css_class = get_watering_status_label(days)
        
        plant_dict['status_label'] = label
        plant_dict['status_class'] = css_class
        processed_plants.append(plant_dict)
        
        if css_class in ['danger', 'warning']:
            urgent_plants.append(plant_dict)
            
    return render_template('dashboard.html', plants=processed_plants, urgent_plants=urgent_plants)

@app.route('/plants/add', methods=['GET', 'POST'])
@login_required
def add_new_plant():
    if request.method == 'POST':
        name = request.form['name']
        species = request.form['species']
        location = request.form['location']
        interval = int(request.form['watering_interval_days'])
        notes = request.form['notes']
        
        add_plant(session['user_id'], name, species, location, interval, notes)
        flash("New plant added to your collection!", "success")
        return redirect(url_for('dashboard'))
        
    return render_template('add_plant.html')

@app.route('/plants/<int:plant_id>')
@login_required
def plant_detail(plant_id):
    plant = get_plant_details(plant_id, session['user_id'])
    if not plant:
        flash("Plant not found in your records.", "danger")
        return redirect(url_for('dashboard'))
        
    history = get_watering_history(plant_id)
    days = days_until_watering(plant['last_watered'], plant['watering_interval_days'])
    label, css_class = get_watering_status_label(days)
    
    return render_template('plant_detail.html', plant=plant, history=history, status_label=label, status_class=css_class)

@app.route('/plants/<int:plant_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_plant_route(plant_id):
    plant = get_plant_details(plant_id, session['user_id'])
    if not plant:
        flash("Plant not found.", "danger")
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        name = request.form['name']
        species = request.form['species']
        location = request.form['location']
        interval = int(request.form['watering_interval_days'])
        notes = request.form['notes']
        
        update_plant(plant_id, session['user_id'], name, species, location, interval, notes)
        flash("Plant information updated.", "success")
        return redirect(url_for('plant_detail', plant_id=plant_id))
        
    return render_template('edit_plant.html', plant=plant)

@app.route('/plants/<int:plant_id>/delete', methods=['POST'])
@login_required
def delete_plant_route(plant_id):
    delete_plant(plant_id, session['user_id'])
    flash("Plant removed from collection.", "info")
    return redirect(url_for('dashboard'))

@app.route('/plants/<int:plant_id>/water', methods=['POST'])
@login_required
def water_plant(plant_id):
    note = request.form.get('note', '')
    log_watering(plant_id, note)
    flash("Watering event recorded!", "success")
    return redirect(url_for('plant_detail', plant_id=plant_id))

if __name__ == "__main__":
    with app.app_context():
        init_db(app)
    # Accessible from any device on the network
    app.run(debug=True, host='0.0.0.0', port=5002)
