import os
from flask import Flask
from webreview.extensions import db, login_manager, bcrypt
from webreview.core.routes import core_bp
from webreview.users.routes import users_bp
from webreview.review.routes import review_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)   

    app.register_blueprint(core_bp,url_prefix='/')
    app.register_blueprint(users_bp,url_prefix='/users')
    app.register_blueprint(review_bp,url_prefix='/review')
    return app