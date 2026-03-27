# SkillSwap - Skill Exchange Platform

SkillSwap is a full-stack web application built with Python Flask that allows users to exchange skills without monetary transactions. It connects people who want to teach what they know with those who want to learn something new.

## Features

- **User Authentication**: Secure registration, login, and logout.
- **Profile Management**: Create and update user profiles with bio, skills, and location.
- **Skill Management**: CRUD operations for skills, categorized by Technical, Creative, Language, etc.
- **Smart Skill Matching**: A simple recommendation system based on common interests (offered vs wanted skills).
- **Exchange Request System**: Send, accept, or reject skill exchange requests.
- **Dashboard**: Track active exchanges, view suggested matches, and manage pending requests.
- **Search and Filter**: Find users by specific skills or categories.
- **Responsive UI**: Modern, clean design using Bootstrap and FontAwesome.

## Tech Stack

- **Backend**: Python, Flask, SQLAlchemy (ORM)
- **Database**: SQLite
- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **Libraries**: Flask-Login, Flask-Bcrypt, scikit-learn (optional for advanced matching)

## How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Seed the Database (Optional but Recommended)**:
   This will create dummy users and skills for testing.
   ```bash
   python seed.py
   ```

3. **Run the Application**:
   ```bash
   python run.py
   ```
   The application will be available at `http://127.0.0.1:5000/`.

## Folder Structure

- `app/`: Main application package
  - `models/`: Database models (User, Skill, ExchangeRequest)
  - `routes/`: Blueprint-based routes (auth, main, profile, skills, exchanges)
  - `templates/`: HTML templates organized by module
  - `static/`: Static files (CSS, JS, images)
- `config.py`: Application configuration
- `run.py`: Entry point for the application
- `seed.py`: Script to populate the database with dummy data
- `requirements.txt`: Project dependencies
