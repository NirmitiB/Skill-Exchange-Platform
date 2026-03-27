from app import db
from datetime import datetime

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=False) # Technical, Creative, Language, etc.
    skill_type = db.Column(db.String(20), nullable=False) # Offered, Wanted
    class_code = db.Column(db.String(50), nullable=True) # Unique code for the skill/class
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Skill('{self.name}', '{self.category}', '{self.skill_type}')"
