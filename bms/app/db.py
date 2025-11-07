from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Initialize the database with the Flask app"""
    db.init_app(app)
    
    with app.app_context():
        # Import models here to ensure they are registered
        from app.models import Account  # noqa
        
        # Create all tables
        db.create_all()