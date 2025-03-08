"""
    • Zweck: Hauptdatei für den Flask-Webserver und API-Endpunkt-Registrierung.
    • Funktionen und Abhängigkeiten wie zuvor dokumentiert
"""

from flask import Flask
from flask_cors import CORS
from routes.filter_routes import filter_routes
from routes.data_routes import data_routes
import os
import logging

# Initialisiere Flask-Anwendung
app = Flask(__name__)

# Lade Konfigurationswerte aus config.py
from models import config
app.config.from_object(config)

# Enable CORS
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if os.environ.get('FLASK_ENV') == 'development' else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Registriere die API-Routen
app.register_blueprint(data_routes)
app.register_blueprint(filter_routes)

# Optional: Initialisiere die Datenbank, falls erforderlich
# from models.database import init_db
# init_db(app)

@app.route('/')
def index():
    return "Welcome to the Battery Failure Visualization API"

@app.route('/health')
def health_check():
    return "OK", 200

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Get debug mode from environment
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    
    try:
        logger.info(f"Starting server on port {port}")
        app.run(
            host='0.0.0.0',
            port=port,
            debug=debug_mode
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")