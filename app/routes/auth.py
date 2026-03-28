from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User

auth = Blueprint('auth', __name__)

@auth.route("/register", methods=['GET', 'POST'])
def register():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            name = request.form.get('name')
            
            # Simple validation
            user_exists = User.query.filter_by(username=username).first()
            email_exists = User.query.filter_by(email=email).first()
            
            if user_exists:
                flash('Username already exists. Please choose a different one.', 'danger')
            elif email_exists:
                flash('Email already registered. Please login.', 'danger')
            else:
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                user = User(username=username, email=email, password=hashed_password, name=name)
                db.session.add(user)
                db.session.commit()
                flash('Your account has been created! You are now able to log in', 'success')
                return redirect(url_for('auth.login'))
                
        return render_template('auth/register.html', title='Register')
    except Exception as e:
        db.session.rollback()
        print(f"REGISTER ERROR: {e}")
        flash('An error occurred during registration. Please try again.', 'danger')
        return render_template('auth/register.html', title='Register')

@auth.route("/login", methods=['GET', 'POST'])
def login():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            remember = True if request.form.get('remember') else False
            
            user = User.query.filter_by(email=email).first()
            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user, remember=remember)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
                
        return render_template('auth/login.html', title='Login')
    except Exception as e:
        print(f"LOGIN ERROR: {e}")
        flash('An error occurred during login. Please try again.', 'danger')
        return render_template('auth/login.html', title='Login')

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))
