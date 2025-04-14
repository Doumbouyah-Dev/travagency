from travency import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    profiles = db.relationship('Profile', backref='user', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    bio = db.Column(db.Text)
    location = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# from my_flask_app import db, login_manager
# from datetime import datetime
# from flask_login import UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash


# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     password_hash = db.Column(db.String(128), nullable=False)
#     registration_date = db.Column(db.DateTime, default=datetime.utcnow)
#     profile = db.relationship('Profile', backref='author', uselist=False)

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)

#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}')"


# class Profile(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     full_name = db.Column(db.String(100))
#     date_of_birth = db.Column(db.Date)
#     location = db.Column(db.String(100))
#     bio = db.Column(db.Text)
#     highest_level_of_education = db.Column(db.String(100))
#     institution_name = db.Column(db.String(100))
#     major = db.Column(db.String(100))
#     graduation_year = db.Column(db.Integer)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

#     def __repr__(self):
#         return f"Profile('{self.full_name}')"