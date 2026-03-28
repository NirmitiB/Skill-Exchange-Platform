from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from flask_login import current_user, login_required
from app import db
from app.models import User, Skill
import os
import secrets
from PIL import Image

profile = Blueprint('profile', __name__)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@profile.route("/profile/<username>")
def view_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    offered_skills = Skill.query.filter_by(user_id=user.id, skill_type='Offered').all()
    wanted_skills = Skill.query.filter_by(user_id=user.id, skill_type='Wanted').all()
    
    return render_template('profile/view.html', 
                           title=f"{user.username}'s Profile", 
                           user=user, 
                           offered_skills=offered_skills, 
                           wanted_skills=wanted_skills)

@profile.route("/profile/edit", methods=['GET', 'POST'])
@login_required
def edit_profile():
    try:
        if request.method == 'POST':
            # Check if picture was uploaded
            if 'picture' in request.files and request.files['picture'].filename != '':
                picture_file = save_picture(request.files['picture'])
                current_user.profile_pic = picture_file
            current_user.name = request.form.get('name')
            current_user.bio = request.form.get('bio')
            current_user.location = request.form.get('location')
            current_user.contact_info = request.form.get('contact_info')
            
            db.session.commit()
            flash('Your profile has been updated!', 'success')
            return redirect(url_for('profile.view_profile', username=current_user.username))
            
        return render_template('profile/edit.html', title='Edit Profile')
    except Exception as e:
        print(f"PROFILE EDIT ERROR: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return f"An internal error occurred during profile update: {e}", 500
