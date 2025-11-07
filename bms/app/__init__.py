import os
from flask import Flask
from app.db import init_db
from app.routes import bp as api_bp
from app.config import Config
from app.logger import logger
# from bms.app.db import init_db
# from bms.app.config import Config
# from bms.app.logger import logger


def create_app(config_class=Config):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Ensure instance path exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Initialize extensions
    init_db(app)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Add a simple health check route to root
    @app.route('/')
    def health_check():
        return {'status': 'healthy', 'service': 'BMS API'}
    
    # Log application startup
    logger.info("application_started", config=app.config.get('ENV', 'development'))
    
    return app