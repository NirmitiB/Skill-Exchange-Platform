from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import current_user, login_required
from app import db
from app.models import Skill

skills = Blueprint('skills', __name__)

@skills.route("/skills/manage")
@login_required
def manage_skills():
    offered_skills = Skill.query.filter_by(user_id=current_user.id, skill_type='Offered').all()
    wanted_skills = Skill.query.filter_by(user_id=current_user.id, skill_type='Wanted').all()
    
    return render_template('skills/manage.html', 
                           title='Manage Skills', 
                           offered_skills=offered_skills, 
                           wanted_skills=wanted_skills)

@skills.route("/skills/add", methods=['GET', 'POST'])
@login_required
def add_skill():
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        skill_type = request.form.get('skill_type') # Offered or Wanted
        class_code = request.form.get('class_code')
        description = request.form.get('description')
        
        skill = Skill(name=name, category=category, skill_type=skill_type, class_code=class_code, description=description, owner=current_user)
        db.session.add(skill)
        db.session.commit()
        
        flash('Skill added successfully!', 'success')
        return redirect(url_for('skills.manage_skills'))
        
    return render_template('skills/add.html', title='Add Skill')

@skills.route("/skills/edit/<int:skill_id>", methods=['GET', 'POST'])
@login_required
def edit_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    if skill.owner != current_user:
        flash('You are not authorized to edit this skill', 'danger')
        return redirect(url_for('skills.manage_skills'))
        
    if request.method == 'POST':
        skill.name = request.form.get('name')
        skill.category = request.form.get('category')
        skill.skill_type = request.form.get('skill_type')
        skill.class_code = request.form.get('class_code')
        skill.description = request.form.get('description')
        
        db.session.commit()
        flash('Skill updated successfully!', 'success')
        return redirect(url_for('skills.manage_skills'))
        
    return render_template('skills/edit.html', title='Edit Skill', skill=skill)

@skills.route("/skills/delete/<int:skill_id>", methods=['POST'])
@login_required
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    if skill.owner != current_user:
        flash('You are not authorized to delete this skill', 'danger')
        return redirect(url_for('skills.manage_skills'))
        
    db.session.delete(skill)
    db.session.commit()
    flash('Skill deleted successfully!', 'success')
    return redirect(url_for('skills.manage_skills'))
