from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from travency import db
from travency.models import User, Profile
from travency.forms import RegistrationForm, LoginForm, ProfileForm
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from datetime import datetime
from flask import send_from_directory
import secrets
from werkzeug.utils import secure_filename


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
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
            preferred_country=form.preferred_country.data,
            preferred_field=form.preferred_field.data,
            education_level=form.education_level.data,
            receive_updates=form.receive_updates.data,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        # Create user upload folder
        folder_name = str(user.id)

        base_upload_path = current_app.config.get('UPLOAD_FOLDER', 'travency/static/uploads')
        user_folder_path = os.path.join(base_upload_path, folder_name)
        os.makedirs(user_folder_path, exist_ok=True)

        
        # user_folder = os.path.join('travency/static/uploads', user.username)
        # os.makedirs(user_folder, exist_ok=True)

        login_user(user)
        flash('Registration successful!', 'success')
        return redirect(url_for('main.index'))

    return render_template('signup.html', form=form)


@main_bp.route("/signin", methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(
            (User.email == form.email_or_phone.data) |
            (User.phone == form.email_or_phone.data)
        ).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Login unsuccessful. Please check your credentials.', 'danger')

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
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.preferred_country = form.preferred_country.data
        current_user.preferred_field = form.preferred_field.data
        current_user.education_level = form.education_level.data
        current_user.about_me = form.about_me.data

        if form.profile_image.data:
            image_file = form.profile_image.data
            filename = secure_filename(image_file.filename)
            ext = filename.rsplit('.', 1)[1].lower()
            new_filename = f"profile.{ext}"
            user_folder = os.path.join('travency/static/uploads', current_user.user.id)
            os.makedirs(user_folder, exist_ok=True)
            image_path = os.path.join(user_folder, new_filename)
            image_file.save(image_path)
            current_user.profile_image = new_filename

        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.profile'))

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

@main_bp.route('/admission', methods=['GET', 'POST'])
@login_required
def admission():
    form = AdmissionForm()
    if form.validate_on_submit():
        user_folder = os.path.join('travency/static/uploads', current_user.id, 'admission')
        os.makedirs(user_folder, exist_ok=True)

        def save_file(file, label):
            filename = secure_filename(file.filename)
            filepath = os.path.join(user_folder, f"{label}_{filename}")
            file.save(filepath)
            upload = Upload(filename=filename, filepath=filepath, filetype=label, user_id=current_user.id)
            db.session.add(upload)

        if form.essay.data:
            save_file(form.essay.data, 'essay')

        if form.transcript.data:
            save_file(form.transcript.data, 'transcript')

        for rec in form.recommendations.data:
            if rec:
                save_file(rec, 'recommendation')

        db.session.commit()
        flash("Your application was successfully submitted!", "success")
        return redirect(url_for('main.success'))

    return render_template('admission.html', form=form)


@main_bp.route('/uploads/<int:user_id>/<path:filename>')
@login_required
def uploaded_file(user_id, filename):
    if username != current_user.id:
        flash("You are not authorized to access this file.", "danger")
        return redirect(url_for('main.index'))

    user_folder = os.path.join('travency/static/uploads', user.id)
    return send_from_directory(user_folder, filename)

@main_bp.route("/my-uploads")
@login_required
def my_uploads():
    uploads = Upload.query.filter_by(user_id=current_user.id).all()
    return render_template("my_uploads.html", uploads=uploads)
