

from flask import Blueprint, render_template, url_for, flash, redirect, request
from travency import db
from travency.models import User, Profile
from travency.forms import RegistrationForm, LoginForm, ProfileForm
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
@main_bp.route("/home")
def index():
    return render_template('index.html')



@main_bp.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user)

       
        return redirect(url_for('main.index'))

    return render_template('signup.html', form=form)



@main_bp.route("/signin", methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')

    return render_template('signin.html', form=form)

@main_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))

    

@main_bp.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.index'))
    return render_template('profile.html', user=current_user, form=form)
    
@main_bp.route("/success")
def success():
    return render_template('success.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/visa-services')
def visa_services():
    return render_template('visa_services.html')

@main_bp.route('/programs')
def programs():
    return render_template('programs.html')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        # Optionally send email here
        flash('Thank you for contacting us!', 'success')
        return redirect(url_for('main.contact'))
    return render_template('contact.html')
