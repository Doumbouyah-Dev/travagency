
# this is the profile form
from wtforms import TextAreaField
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, BooleanField,
    TextAreaField, DateField, SelectField, MultipleFileField, FileField
)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from travency.models import User
from flask_wtf.file import FileField, FileAllowed

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    preferred_country = StringField('Preferred Country of Study')
    preferred_field = StringField('Preferred Field of Study')
    education_level = StringField('Highest Level of Education Completed')
    receive_updates = BooleanField('Receive Updates and Newsletters')
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered.')

    def validate_phone(self, phone):
        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('That phone number is already registered.')



class LoginForm(FlaskForm):
    email_or_phone = StringField('Email or Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')



            

class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    preferred_country = StringField('Preferred Country of Study')
    preferred_field = StringField('Preferred Field of Study')
    education_level = StringField('Highest Level of Education Completed')
    about_me = TextAreaField('About Me', validators=[Length(max=500)])
    profile_image = FileField('Profile Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update Profile')


class ContactForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')


from wtforms import DateField, SelectField, MultipleFileField

class AdmissionForm(FlaskForm):
    full_name = StringField('Full Legal Name', validators=[DataRequired()])
    preferred_name = StringField('Preferred Name')
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d')
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    phone = StringField('Phone Number', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    address = StringField('Mailing Address')
    citizenship = StringField('Citizenship')
    country_of_birth = StringField('Country of Birth')

    high_school = StringField('High School Name')
    hs_location = StringField('High School Location')
    hs_dates = StringField('Dates Attended')
    hs_gpa = StringField('GPA')
    hs_certificate = StringField('Diploma/Certificate')

    college = StringField('College Name (if any)')
    college_location = StringField('College Location')
    college_dates = StringField('College Attendance Dates')
    college_gpa = StringField('College GPA')

    test_scores = TextAreaField('Test Scores (SAT, TOEFL, etc.)')
    extracurriculars = TextAreaField('Extracurricular Activities, Honors, Awards')
    essay = FileField('Upload Personal Statement/Essay', validators=[FileAllowed(['pdf', 'doc', 'docx'])])
    transcript = FileField('Upload Transcript', validators=[FileAllowed(['pdf', 'doc', 'docx', 'jpg', 'png'])])
    recommendations = MultipleFileField('Upload Recommendation Letters', validators=[FileAllowed(['pdf', 'doc', 'docx'])])

    submit = SubmitField('Submit Application')
