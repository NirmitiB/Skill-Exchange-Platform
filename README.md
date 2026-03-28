# SkillSwap - Skill Exchange Platform

SkillSwap is a full-stack web application built with Python Flask that allows users to exchange skills without monetary transactions. It connects people who want to teach what they know with those who want to learn something new.

---

## 🚀 Features

* User Authentication (Register, Login, Logout)
* Profile Management (Bio, Skills, Location)
* Skill Management (Add, Edit, Delete)
* Smart Skill Matching System
* Exchange Request System (Send, Accept, Reject)
* Dashboard with activity tracking
* Search and filter users by skills
* Responsive UI using Bootstrap

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask, SQLAlchemy
* **Database:** SQLite
* **Frontend:** HTML, CSS (Bootstrap), JavaScript
* **Libraries:** Flask-Login, Flask-Bcrypt, scikit-learn 

---

## ⚙️ How to Run the Project

### 1. Clone or Download the Project

Download ZIP or clone using Git:

```
git clone https://github.com/NirmitiB/Skill-Exchange-Platform.git
```

---

### 2. Navigate to Project Folder

```
cd Skill-Exchange-Platform
```

---

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

### 4. Seed the Database

This step adds sample users and skills for testing:

```
python seed.py
```

---

### 5. Run the Application

```
python run.py
```

---

### 6. Open in Browser

Go to:

```
http://127.0.0.1:5000/
```

---

## 📁 Project Structure

* `app/` – Main application

  * `models/` – Database models
  * `routes/` – Application routes
  * `templates/` – HTML files
  * `static/` – CSS, JS, images
* `config.py` – Configuration settings
* `run.py` – Application entry point
* `seed.py` – Dummy data script
* `requirements.txt` – Dependencies

---

## 📌 Notes

* Make sure Python 3 is installed
* Internet may be required for some features
* Database will be created automatically if not present

---
