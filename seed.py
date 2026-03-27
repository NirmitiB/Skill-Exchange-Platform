from app import create_app, db, bcrypt
from app.models import User, Skill, ExchangeRequest
from datetime import datetime

def seed_data():
    app = create_app()
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create dummy users
        users = [
            {
                "username": "alice_coder",
                "email": "alice@example.com",
                "password": "password123",
                "name": "Alice Johnson",
                "bio": "Full-stack developer with a passion for teaching Python and learning creative arts.",
                "location": "New York, USA"
            },
            {
                "username": "bob_designer",
                "email": "bob@example.com",
                "password": "password123",
                "name": "Bob Smith",
                "bio": "Graphic designer specializing in UI/UX and brand identity. Looking to pick up some coding skills.",
                "location": "London, UK"
            },
            {
                "username": "charlie_polyglot",
                "email": "charlie@example.com",
                "password": "password123",
                "name": "Charlie Davis",
                "bio": "Fluent in 5 languages. Love sharing linguistic knowledge and learning about world history.",
                "location": "Paris, France"
            },
            {
                "username": "david_chef",
                "email": "david@example.com",
                "password": "password123",
                "name": "David Wilson",
                "bio": "Professional chef with 10 years of experience. Can teach anything from baking to gourmet cooking.",
                "location": "Tokyo, Japan"
            }
        ]

        created_users = []
        for u in users:
            hashed_password = bcrypt.generate_password_hash(u["password"]).decode('utf-8')
            user = User(
                username=u["username"],
                email=u["email"],
                password=hashed_password,
                name=u["name"],
                bio=u["bio"],
                location=u["location"]
            )
            db.session.add(user)
            created_users.append(user)
        
        db.session.commit()

        # Add dummy skills
        skills = [
            # Alice's skills
            {"name": "Python Programming", "category": "Technical", "skill_type": "Offered", "user_id": created_users[0].id, "description": "Can teach Flask, Django, and Data Science basics.", "class_code": "PY-ALICE-101"},
            {"name": "ReactJS", "category": "Technical", "skill_type": "Offered", "user_id": created_users[0].id, "description": "Expert in building modern web apps with React.", "class_code": "JS-REACT-MASTER"},
            {"name": "Graphic Design", "category": "Creative", "skill_type": "Wanted", "user_id": created_users[0].id, "description": "Looking to learn Figma and Adobe Illustrator."},
            {"name": "Cooking", "category": "Lifestyle", "skill_type": "Wanted", "user_id": created_users[0].id, "description": "Want to learn basic culinary skills."},

            # Bob's skills
            {"name": "UI/UX Design", "category": "Creative", "skill_type": "Offered", "user_id": created_users[1].id, "description": "Can teach wireframing, prototyping, and user research.", "class_code": "DESIGN-BOB-UI"},
            {"name": "Logo Design", "category": "Creative", "skill_type": "Offered", "user_id": created_users[1].id, "description": "Specialized in creating memorable brand identities.", "class_code": "LOGO-EXPERT-99"},
            {"name": "Python Programming", "category": "Technical", "skill_type": "Wanted", "user_id": created_users[1].id, "description": "Interested in automating design workflows with Python."},
            {"name": "French Language", "category": "Language", "skill_type": "Wanted", "user_id": created_users[1].id, "description": "Beginner looking to learn basic French."},

            # Charlie's skills
            {"name": "French Language", "category": "Language", "skill_type": "Offered", "user_id": created_users[2].id, "description": "Native speaker. Can help with grammar and conversation.", "class_code": "FR-CHARLIE-PARIS"},
            {"name": "Spanish Language", "category": "Language", "skill_type": "Offered", "user_id": created_users[2].id, "description": "Fluent speaker. Focus on Latin American Spanish.", "class_code": "ES-SPANISH-MEX"},
            {"name": "ReactJS", "category": "Technical", "skill_type": "Wanted", "user_id": created_users[2].id, "description": "Want to learn web development basics."},

            # David's skills
            {"name": "Gourmet Cooking", "category": "Lifestyle", "skill_type": "Offered", "user_id": created_users[3].id, "description": "Professional culinary techniques and plating.", "class_code": "CHEF-DAVID-MEAL"},
            {"name": "Baking", "category": "Lifestyle", "skill_type": "Offered", "user_id": created_users[3].id, "description": "Can teach bread making and pastry arts.", "class_code": "BAKE-WITH-DAVID"},
            {"name": "Spanish Language", "category": "Language", "skill_type": "Wanted", "user_id": created_users[3].id, "description": "Want to learn Spanish for traveling."}
        ]

        for s in skills:
            skill = Skill(**s)
            db.session.add(skill)
        
        db.session.commit()

        print("Database seeded successfully with dummy data!")

if __name__ == "__main__":
    seed_data()
