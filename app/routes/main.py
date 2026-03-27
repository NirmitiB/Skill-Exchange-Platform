from flask import Blueprint, render_template, request, current_app, redirect, url_for
from flask_login import login_required, current_user
from app.models import User, Skill, ExchangeRequest
from sqlalchemy import or_

main = Blueprint('main', __name__)

@main.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('main/index.html')

@main.route("/home")
def home():
    return render_template('main/index.html')

@main.route("/dashboard")
@login_required
def dashboard():
    # Get user's skills
    offered_skills = [s.name.lower() for s in current_user.skills if s.skill_type == 'Offered']
    wanted_skills = [s.name.lower() for s in current_user.skills if s.skill_type == 'Wanted']
    
    # Simple recommendation system
    recommended_users = []
    if wanted_skills or offered_skills:
        # Find users who offer what I want OR want what I offer
        potential_matches = User.query.filter(User.id != current_user.id).all()
        
        for user in potential_matches:
            user_offered = [s.name.lower() for s in user.skills if s.skill_type == 'Offered']
            user_wanted = [s.name.lower() for s in user.skills if s.skill_type == 'Wanted']
            
            # Check for matches
            # 1. They offer what I want
            match_score = 0
            for skill in wanted_skills:
                if skill in user_offered:
                    match_score += 2
            
            # 2. I offer what they want
            for skill in offered_skills:
                if skill in user_wanted:
                    match_score += 1
            
            if match_score > 0:
                recommended_users.append({'user': user, 'score': match_score})
        
        # Sort by score descending
        recommended_users = sorted(recommended_users, key=lambda x: x['score'], reverse=True)[:5]

    # Get recent exchanges
    active_exchanges = ExchangeRequest.query.filter(
        or_(ExchangeRequest.sender_id == current_user.id, ExchangeRequest.receiver_id == current_user.id),
        ExchangeRequest.status == 'Accepted'
    ).order_by(ExchangeRequest.date_sent.desc()).limit(5).all()
    
    pending_requests = ExchangeRequest.query.filter(
        ExchangeRequest.receiver_id == current_user.id,
        ExchangeRequest.status == 'Pending'
    ).order_by(ExchangeRequest.date_sent.desc()).all()

    return render_template('main/dashboard.html', 
                           title='Dashboard',
                           recommended_users=recommended_users,
                           active_exchanges=active_exchanges,
                           pending_requests=pending_requests)

@main.route("/search")
@login_required
def search():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    users_query = User.query.filter(User.id != current_user.id)
    
    if query:
        users_query = users_query.join(Skill).filter(
            or_(
                Skill.name.ilike(f'%{query}%'),
                User.name.ilike(f'%{query}%'),
                User.username.ilike(f'%{query}%')
            )
        )
    
    if category:
        users_query = users_query.join(Skill).filter(Skill.category == category)
        
    results = users_query.distinct().all()
    
    return render_template('main/search_results.html', title='Search Results', results=results, query=query)

