from app import create_app, db
from app.models import User, Skill

app = create_app()
with app.app_context():
    user = User.query.filter_by(username='nirmiti').first()
    if user:
        # Add a skill you offer
        s1 = Skill(name="Python", category="Technical", skill_type="Offered", user_id=user.id, description="I can help with basic Python scripts.")
        # Add a skill you want
        s2 = Skill(name="French", category="Language", skill_type="Wanted", user_id=user.id, description="I want to learn conversational French.")
        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()
        print("Successfully added skills for nirmiti!")
    else:
        print("User nirmiti not found.")
