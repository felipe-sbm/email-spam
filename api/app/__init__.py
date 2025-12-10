from flask import Flask
from flask_cors import CORS
from app.config import config
from app.models.email import db

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Register blueprints
    from app.routes import prediction, emails
    app.register_blueprint(prediction.bp)
    app.register_blueprint(emails.bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
        
    return app
