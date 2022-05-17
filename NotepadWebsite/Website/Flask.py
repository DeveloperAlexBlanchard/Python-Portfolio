from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


# SQL Database adds Users to the Database
db = SQLAlchemy()
DB_NAME = "database.db"


# Function to create the application
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'TOTALLY_NOT_A_SECRET_KEY'


    # SQL Alchemy Database is stored
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Import Views and Authenticate files
    from .views import views
    from .authenticate import auth

    # Register the Blueprints for Authentication and Views
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import Models File
    from .models import User, Note

    create_database(app)

    # Authenticate User Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    # Create User's Database if One does not Already Exist
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
