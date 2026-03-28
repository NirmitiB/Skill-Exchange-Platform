from flask import Blueprint, request, jsonify
from flask_login import current_user
import random

chatbot = Blueprint('chatbot', __name__)

# Expanded Knowledge base for the platform
KNOWLEDGE_BASE = {
    "hello": ["Hello! How can I help you navigate the SkillSwap world today?", "Hi there! I'm your SkillSwap assistant. Ready to help you learn something new?"],
    "how are you": ["I'm powered up and ready to help you find the perfect skill match!", "Doing great! The community is growing and I'm here to support your learning journey."],
    
    # Platform Basics
    "what is this": ["SkillSwap is a community platform where people trade their expertise. You teach what you know, and in return, you learn what you want—no money required!", "This is a peer-to-peer learning network designed to make education accessible through direct human interaction."],
    "who are you": ["I'm the SkillSwap AI assistant. I'm here to explain how the platform works, help you manage your skills, and guide you through the exchange process.", "I'm your digital guide to SkillSwap. Think of me as your personal tutor for using this platform!"],
    
    # Skill Management
    "add skill": ["To add a skill, go to 'Manage Skills' in the navbar and click 'Add New Skill'. You can list skills you want to teach (Offered) or skills you want to learn (Wanted).", "Head over to the 'Manage Skills' page. There, you can define your expertise and your learning goals."],
    "class code": ["A Class Code or Zoom ID is a unique link or identifier you provide when adding an offered skill. It's shared with your partner ONLY after you both accept an exchange.", "Class codes allow you to set up virtual classrooms. They are kept private until an exchange is activated."],
    "delete skill": ["You can remove any skill by going to 'Manage Skills' and using the dropdown menu (three dots) on the skill card.", "Changed your mind? Just go to 'Manage Skills' and click 'Delete' on any skill you no longer wish to offer or learn."],
    "categories": ["We support many categories: Technical (coding, data), Creative (design, music), Language (French, Spanish), Lifestyle (cooking, fitness), and more!", "You can categorize your skills into groups like Technical, Creative, Language, or Lifestyle to help our AI match you better."],
    
    # Exchange Process
    "how to swap": ["It's a 3-step process: 1. Add your skills. 2. Search for a partner or check your 'AI Recommendations'. 3. Click 'Send Exchange Request' on their profile.", "To start swapping, find someone whose 'Offered' skill matches your 'Wanted' skill and send them a request from their profile page."],
    "accept": ["When someone sends you a request, it appears under 'Pending Requests' on your dashboard. Clicking 'Accept' activates the exchange and reveals contact details.", "Accepting a request means you agree to swap skills. Once you click 'Accept', you'll see the partner's Gmail and Class Code."],
    "reject": ["If a request doesn't fit your schedule or interests, you can click 'Reject'. This will notify the sender and remove the request from your list.", "Don't worry about saying no! If a match isn't right, just click 'Reject' to keep your dashboard clean."],
    "cancel": ["If you sent a request by mistake, you can go to 'My Exchanges' and click 'Cancel' on any pending request you've sent.", "You can always withdraw a sent request from the 'My Exchanges' page before the other person responds."],
    
    # Interaction & Privacy
    "contact": ["For privacy, we only reveal Gmail addresses and Class Codes after an exchange is 'Accepted'. You can find these in the 'My Exchanges' section.", "Once an exchange is active, go to 'My Exchanges' to see your partner's contact info and start your lesson!"],
    "gmail": ["We share the user's Gmail ID only after mutual acceptance so you can coordinate your learning sessions directly via email.", "Your email is protected until you and your partner both agree to the exchange."],
    "zoom": ["Many users use the 'Class Code' field to provide Zoom or Google Meet links for their sessions.", "You can interact via Zoom, Google Meet, or even in person! Just coordinate with your partner using the contact info provided after acceptance."],
    
    # Profile
    "profile": ["Your profile shows your bio, location, and the skills you offer/want. You can customize it by clicking 'Edit Profile' from the user menu.", "Make your profile stand out by adding a detailed bio and a professional profile picture!"],
    "picture": ["You can upload a profile picture in the 'Edit Profile' section. We recommend a clear photo so your partners can recognize you.", "Adding a profile picture helps build trust in the community. Upload one from your account settings."],
    "location": ["Adding your location is optional but helps you find local partners if you prefer in-person skill swapping.", "You can specify your city or country in your profile settings to connect with learners nearby."],
    
    # Advanced
    "matching": ["Our 'Smart Match' AI analyzes your profile to find users who have what you want and want what you have. Check your dashboard for these suggestions!", "The AI looks for overlapping interests. For example, if you offer 'Python' and want 'Guitar', it finds people who offer 'Guitar' and want 'Python'."],
    "search": ["Use the search bar in the navbar to find specific skills, categories, or users by their name.", "Looking for something specific? Just type the skill name into the search bar at the top of any page."],
    
    # Social
    "thanks": ["You're very welcome! Happy learning!", "No problem! I'm here if you have more questions.", "Anytime! Go out there and swap some awesome skills!"],
    "bye": ["Goodbye! See you in the community!", "Happy swapping! Don't forget to check your dashboard for new requests.", "See you later! Keep learning!"],
    
    "default": ["I'm not quite sure about that. Try asking about 'how to swap', 'class codes', 'matching', or 'profile'!", "Interesting question! You can find more details in the 'Dashboard' or 'My Exchanges' sections.", "I'm still learning! Try using simpler keywords like 'add skill', 'accept request', or 'privacy'."]
}

@chatbot.route("/chatbot/query", methods=['POST'])
def query():
    try:
        data = request.json
        if not data or 'message' not in data:
            return jsonify({"response": "I'm listening! What would you like to know about SkillSwap?"})
            
        message = data.get('message', '').lower()
        
        # Priority matching logic
        best_match = None
        highest_score = 0
        
        for key in KNOWLEDGE_BASE:
            # Check for exact matches or partial keyword matches
            if key in message:
                # Score based on keyword length (longer keywords are more specific)
                score = len(key)
                if score > highest_score:
                    highest_score = score
                    best_match = key
        
        if best_match:
            response = random.choice(KNOWLEDGE_BASE[best_match])
        else:
            response = random.choice(KNOWLEDGE_BASE["default"])
            
        return jsonify({"response": response})
    except Exception as e:
        print(f"CHATBOT ERROR: {e}")
        return jsonify({"response": "I encountered a small hiccup. Could you try asking that again?"})
