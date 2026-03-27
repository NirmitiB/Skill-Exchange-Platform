from app import db
from datetime import datetime

class ExchangeRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Skill being offered by sender or requested from receiver
    # To keep it simple, sender offers a skill in exchange for a skill receiver offers
    skill_offered_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=True)
    skill_wanted_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=True)
    
    status = db.Column(db.String(20), nullable=False, default='Pending') # Pending, Accepted, Rejected
    message = db.Column(db.Text, nullable=True)
    date_sent = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationship to Skills
    skill_offered = db.relationship('Skill', foreign_keys=[skill_offered_id], backref='offered_exchanges')
    skill_wanted = db.relationship('Skill', foreign_keys=[skill_wanted_id], backref='wanted_exchanges')

    def __repr__(self):
        return f"ExchangeRequest('{self.sender_id}' -> '{self.receiver_id}', '{self.status}')"
