# 🌿 PlantTracker: Advanced Plant Care Management System

## 📌 Project Overview
**PlantTracker** is a comprehensive web application built with Python and Flask, designed to simplify indoor gardening by tracking watering schedules and care history. This project serves as the final submission for the **Spring 2026 Software Engineering** course, demonstrating proficiency in full-stack development, relational database management, and user-centric design.

### Key Objectives
*   **Data Persistence:** Robust storage of user and plant data using SQLite.
*   **User Security:** Secure authentication using industry-standard hashing.
*   **Operational Efficiency:** Automated calculations for plant care deadlines.
*   **Clean Architecture:** Modular code structure following the MVC pattern.

---

## 📋 User Stories & Detailed Acceptance Criteria

This project adheres to the specific requirements outlined in the course guidelines. Below is the mapping of user stories to system functionality.

| ID | User Story | Acceptance Criteria | Status |
| :--- | :--- | :--- | :--- |
| **US1** | **Account Management** | - Users can register with unique credentials.<br>- Passwords must be hashed (PBKDF2).<br>- Session-based login/logout. | ✅ Done |
| **US2** | **Privacy & Isolation** | - Users can only access their own data.<br>- Unauthorized access to plant IDs is blocked via backend checks. | ✅ Done |
| **US3** | **Plant CRUD** | - Full Create, Read, Update, Delete for plant entities.<br>- Input validation for mandatory fields. | ✅ Done |
| **US4** | **Smart Scheduling** | - Automatic calculation of "Days Until Watering".<br>- Visual status indicators (Overdue, Today, Future). | ✅ Done |
| **US5** | **Care History** | - Users can log each watering event with optional notes.<br>- History is displayed in reverse chronological order. | ✅ Done |

---

## 🏗️ Technical Architecture

### 1. Backend Stack
*   **Framework:** Flask 3.x
*   **Language:** Python 3.11+
*   **Authentication:** Werkzeug Security (generate_password_hash, check_password_hash)
*   **Session Management:** Flask-Session (Client-side signed cookies)

### 2. Database Design (Relational Schema)
The system uses a relational SQLite database. No ORM was used, adhering to the requirement for **Raw SQL**.

#### **ER Diagram Logic:**
*   `users` (1) <---> (N) `plants`
*   `plants` (1) <---> (N) `watering_logs`

#### **Table Structures:**
```sql
-- Users Table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

-- Plants Table
CREATE TABLE plants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    watering_interval_days INTEGER NOT NULL,
    last_watered TEXT, -- ISO format date
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

### 3. Frontend Stack
*   **Templating:** Jinja2 (Inheritance used for `base.html`)
*   **Styling:** Custom CSS3 with a focus on "Nature-inspired" green palette.
*   **Responsiveness:** Mobile-first approach using Flexbox and Grid.

---

## 🛠️ Installation & Deployment

### Prerequisites
*   Python 3.10 or higher
*   pip (Python package manager)

### Step-by-Step Setup
1.  **Clone & Navigate:**
    ```bash
    git clone https://github.com/muhammet-taha-dmr/plant_care_app.git
    cd plant-care-app
    ```
2.  **Environment Setup:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3.  **Dependency Installation:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Database Initialization:**
    The database initializes automatically on the first run of the application.
5.  **Execution:**
    ```bash
    python app.py
    ```
    *The app will be available at `http://localhost:5002`*

---

## 🔍 Quality Assurance & Testing

### Unit Testing
The project includes basic unit tests for business logic in `tests/`.
*   **Tested Logic:** Watering interval calculations, data validation strings.
*   **Run Tests:** `pytest tests/`

### Security Measures
*   **SQL Injection Prevention:** All queries use parameterized inputs (`?` placeholders).
*   **XSS Protection:** Jinja2 auto-escaping is enabled for all templates.
*   **Access Control:** `login_required` decorator protects all sensitive routes.

---

## 📂 Project Structure
```text
├── app.py           # Main application entry point & routing
├── auth.py          # User authentication logic
├── plants.py        # Plant-related CRUD operations
├── database.py      # SQLite connection & initialization
├── utils.py         # Business logic & helper functions
├── schema.sql       # Database table definitions
├── static/          # CSS and assets
├── templates/       # Jinja2 HTML templates
└── tests/           # Unit tests for core logic
```


---
**Course:** Arel University Software Engineering Final Project  
**Date:** May 2026  
**Status:** Functional & Ready for Demo
