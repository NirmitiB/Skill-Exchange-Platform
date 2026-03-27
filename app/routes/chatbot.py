from flask import Blueprint, request, jsonify
from flask_login import current_user
import random

chatbot = Blueprint('chatbot', __name__)

# Knowledge base for the platform
KNOWLEDGE_BASE = {
    "hello": ["Hello! How can I help you today?", "Hi there! I'm your SkillSwap assistant. What's on your mind?", "Hey! Ready to swap some skills?"],
    "how are you": ["I'm doing great, especially when I'm helping people swap skills!", "I'm functioning perfectly. Ready to assist you!"],
    "what is this": ["SkillSwap is a platform where you can trade your expertise for something new without any money involved.", "This is a skill exchange platform for learning and teaching in a community-driven way."],
    "how to swap": ["To swap skills, first add your skills in the 'Manage Skills' section. Then search for users who offer what you want and send them an exchange request!", "It's easy! Add your skills, find a match on your dashboard, and click 'Send Exchange Request' on their profile."],
    "matching": ["Our AI analyzes the 'Skills Offered' and 'Skills Wanted' across all users to find the most compatible matches for you. You can see these on your dashboard!", "The 'Smart Match' system uses keyword analysis to suggest people who have what you want and want what you have."],
    "requests": ["You can track all your sent and received requests in the 'My Exchanges' section.", "Go to 'My Exchanges' to see if someone has accepted your request or if you have new ones waiting."],
    "profile": ["You can update your bio, location, and name in the 'Edit Profile' section.", "Click on your username in the navbar and select 'My Profile' to see how others see you."],
    "delete skill": ["Go to 'Manage Skills' and click the three dots next to any skill to find the delete option.", "You can remove any skill you've added from the 'Manage Skills' page."],
    "who are you": ["I'm the SkillSwap AI assistant, here to help you navigate the platform and answer your questions!", "I'm your friendly neighborhood chatbot, powered by SkillSwap's logic."],
    "thanks": ["You're very welcome!", "Happy to help!", "Anytime! Let me know if you need anything else."],
    "bye": ["Goodbye! Happy skill swapping!", "See you later! Don't forget to check your requests."],
    "default": ["That's a great question! I'm still learning, but you can find most information in the 'Dashboard' or by exploring the 'Manage Skills' section.", "I'm not quite sure about that. Try asking about 'how to swap', 'matching', or 'profile'!", "Interesting! I'd recommend checking the dashboard for our AI-powered recommendations."]
}

@chatbot.route("/chatbot/query", methods=['POST'])
def query():
    data = request.json
    message = data.get('message', '').lower()
    
    response = ""
    # Simple keyword matching logic
    for key in KNOWLEDGE_BASE:
        if key in message:
            response = random.choice(KNOWLEDGE_BASE[key])
            break
            
    if not response:
        response = random.choice(KNOWLEDGE_BASE["default"])
        
    return jsonify({"response": response})
