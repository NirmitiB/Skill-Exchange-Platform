from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import current_user, login_required
from app import db
from app.models import User, Skill, ExchangeRequest
from sqlalchemy import or_

exchanges = Blueprint('exchanges', __name__)

@exchanges.route("/exchanges/list")
@login_required
def list_exchanges():
    # Requests I've sent
    sent_requests = ExchangeRequest.query.filter_by(sender_id=current_user.id).order_by(ExchangeRequest.date_sent.desc()).all()
    # Requests I've received
    received_requests = ExchangeRequest.query.filter_by(receiver_id=current_user.id).order_by(ExchangeRequest.date_sent.desc()).all()
    
    return render_template('exchanges/list.html', 
                           title='My Exchanges', 
                           sent_requests=sent_requests, 
                           received_requests=received_requests)

@exchanges.route("/exchanges/request/<username>", methods=['GET', 'POST'])
@login_required
def send_request(username):
    try:
        receiver = User.query.filter_by(username=username).first_or_404()
        if receiver == current_user:
            flash("You cannot send a request to yourself.", "warning")
            return redirect(url_for('main.dashboard'))
            
        if request.method == 'POST':
            skill_offered_id = request.form.get('skill_offered_id')
            skill_wanted_id = request.form.get('skill_wanted_id')
            message = request.form.get('message')
            
            exchange_request = ExchangeRequest(
                sender_id=current_user.id,
                receiver_id=receiver.id,
                skill_offered_id=skill_offered_id,
                skill_wanted_id=skill_wanted_id,
                message=message
            )
            db.session.add(exchange_request)
            db.session.commit()
            
            flash(f'Exchange request sent to {receiver.username}!', 'success')
            return redirect(url_for('exchanges.list_exchanges'))
            
        # Get current user's offered skills and receiver's offered skills
        my_offered_skills = Skill.query.filter_by(user_id=current_user.id, skill_type='Offered').all()
        receiver_offered_skills = Skill.query.filter_by(user_id=receiver.id, skill_type='Offered').all()
        
        return render_template('exchanges/request.html', 
                               title='Send Exchange Request', 
                               receiver=receiver,
                               my_offered_skills=my_offered_skills,
                               receiver_offered_skills=receiver_offered_skills)
    except Exception as e:
        db.session.rollback()
        print(f"SEND REQUEST ERROR: {e}")
        flash('An error occurred while sending the request.', 'danger')
        return redirect(url_for('main.dashboard'))

@exchanges.route("/exchanges/accept/<int:request_id>", methods=['POST'])
@login_required
def accept_request(request_id):
    try:
        exchange_request = ExchangeRequest.query.get_or_404(request_id)
        if exchange_request.receiver_id != current_user.id:
            flash('Unauthorized action.', 'danger')
            return redirect(url_for('exchanges.list_exchanges'))
            
        exchange_request.status = 'Accepted'
        db.session.commit()
        flash('Exchange request accepted!', 'success')
        return redirect(url_for('exchanges.list_exchanges'))
    except Exception as e:
        db.session.rollback()
        print(f"ACCEPT REQUEST ERROR: {e}")
        flash('An error occurred while accepting the request.', 'danger')
        return redirect(url_for('exchanges.list_exchanges'))

@exchanges.route("/exchanges/reject/<int:request_id>", methods=['POST'])
@login_required
def reject_request(request_id):
    try:
        exchange_request = ExchangeRequest.query.get_or_404(request_id)
        if exchange_request.receiver_id != current_user.id:
            flash('Unauthorized action.', 'danger')
            return redirect(url_for('exchanges.list_exchanges'))
            
        exchange_request.status = 'Rejected'
        db.session.commit()
        flash('Exchange request rejected.', 'info')
        return redirect(url_for('exchanges.list_exchanges'))
    except Exception as e:
        db.session.rollback()
        print(f"REJECT REQUEST ERROR: {e}")
        flash('An error occurred while rejecting the request.', 'danger')
        return redirect(url_for('exchanges.list_exchanges'))

@exchanges.route("/exchanges/cancel/<int:request_id>", methods=['POST'])
@login_required
def cancel_request(request_id):
    try:
        exchange_request = ExchangeRequest.query.get_or_404(request_id)
        if exchange_request.sender_id != current_user.id:
            flash('Unauthorized action.', 'danger')
            return redirect(url_for('exchanges.list_exchanges'))
            
        db.session.delete(exchange_request)
        db.session.commit()
        flash('Exchange request cancelled.', 'info')
        return redirect(url_for('exchanges.list_exchanges'))
    except Exception as e:
        db.session.rollback()
        print(f"CANCEL REQUEST ERROR: {e}")
        flash('An error occurred while cancelling the request.', 'danger')
        return redirect(url_for('exchanges.list_exchanges'))
