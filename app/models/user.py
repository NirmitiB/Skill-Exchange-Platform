from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    contact_info = db.Column(db.String(200), nullable=True) # For email, Zoom link, etc.
    profile_pic = db.Column(db.String(20), nullable=False, default='default.jpg')
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    skills = db.relationship('Skill', backref='owner', lazy=True, cascade="all, delete-orphan")
    
    # Requests sent by this user
    requests_sent = db.relationship('ExchangeRequest', 
                                   foreign_keys='ExchangeRequest.sender_id', 
                                   backref='sender', lazy=True,
                                   cascade="all, delete-orphan")
    
    # Requests received by this user
    requests_received = db.relationship('ExchangeRequest', 
                                       foreign_keys='ExchangeRequest.receiver_id', 
                                       backref='receiver', lazy=True,
                                       cascade="all, delete-orphan")

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
