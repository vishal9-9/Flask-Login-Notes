import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import mysql.connector
import pymysql

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "abhjgfadjhadkjhfcsdf"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/users'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from website import views
    from website import auth
    app.register_blueprint(views.views,prefix='/')
    app.register_blueprint(auth.auth,prefix='/')
    from website import models
    #create_db(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return models.Users.query.get(int(id))
    
    return app



def create_db(app):
    if not os.path.exists("/users.db"):
        my_db = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = "password"
        )
        my_cursor = my_db.cursor()
        my_cursor.execute("CREATE DATABASE users")
        db.create_all(app=app)
