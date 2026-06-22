from flask import Flask
from app.config import Config
from app.extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize config
    config_class.init_app(app)

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints / Routes
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
