from flask import render_template, url_for, flash, redirect, request
from travency  import app, db
from travency.models import User, Profile
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash


@app.route("/")
@app.route("/home")
def index():
    return render_template('index.html')


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))  # Redirect logged-in users
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('signup'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('signup'))

        if User.query.filter_by(username=username).first():
            flash('Username already taken.', 'danger')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        user = User(email=email, username=username, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please sign in.', 'success')
        return redirect(url_for('signin'))
    return render_template('signup.html')


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username_or_email = request.form['username_or_email']
        password = request.form['password']
        user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('profile'))
        else:
            flash('Invalid username/email or password.', 'danger')
            return redirect(url_for('signin'))
    return render_template('signin.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.profile.full_name = request.form['full_name']
        current_user.profile.date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d') if request.form['date_of_birth'] else None
        current_user.profile.location = request.form['location']
        current_user.profile.bio = request.form['bio']
        current_user.profile.highest_level_of_education = request.form['highest_level_of_education']
        current_user.profile.institution_name = request.form['institution_name']
        current_user.profile.major = request.form['major']
        current_user.profile.graduation_year = int(request.form['graduation_year']) if request.form['graduation_year'] else None
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    return render_template('profile.html', profile=current_user.profile)