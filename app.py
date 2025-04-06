import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') # get secret key from environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'signin'
login_manager.login_message_category = 'info'

from tra import routes

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    if __name__ == '__main__':
        with app.app_context():
            db.create_all()
        app.run(host='0.0.0.0', debug=True) # host set to 0.0.0.0