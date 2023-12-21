from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from os import path 
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db" # sets the name for the SQLite database file

def create_app(): # creates the Flask application
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app) 
    

    
    from .views import views
    from .auth import auth 
    
    app.register_blueprint(views)
    app.register_blueprint(auth)
    
    from .models import User  
    
    with app.app_context():
        db.create_all()    # creates database tables based on the defined models
        
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader 
    def load_user(id):
        return User.query.get(int(id)) 
    
    
    return app

def create_database(app): # checks if the database file exists
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
        

