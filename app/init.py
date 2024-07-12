from flask import Flask
from flask_migrate import Migrate
from app.config import DevelopmentConfig, ProductionConfig
from app.extensions import db, bcrypt, jwt

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    migrate = Migrate(app, db)

    from app.routes.account_routes import account_bp
    app.register_blueprint(account_bp, url_prefix='/api/accounts')

    return app
3. app/extensions.py
python
Copy code
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()