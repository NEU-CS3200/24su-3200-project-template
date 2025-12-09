from flask import Flask
from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler

from backend.db_connection import db
from backend.dataAnalysts.dataAnalyst_routes import dataAnalyst
from backend.admin.admin_routes import admin

from backend.taker.taker_routes import taker
from backend.swapper.swapper_routes import swapper

logging.basicConfig(level=logging.DEBUG)



def create_app():
    app = Flask(__name__)

    app.logger.setLevel(logging.DEBUG)
    app.logger.info('API startup')

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # # these are for the DB object to be able to connect to MySQL.
    # app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config["MYSQL_DATABASE_USER"] = os.getenv("DB_USER", "root").strip()
    app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("MYSQL_ROOT_PASSWORD", "password").strip()
    app.config["MYSQL_DATABASE_HOST"] = os.getenv("DB_HOST", "db").strip()
    app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("DB_PORT", "3306").strip())
    app.config["MYSQL_DATABASE_DB"] = os.getenv("DB_NAME", "fithub").strip()

    # Initialize the database object with the settings above.
    app.logger.info("current_app(): starting the database connection")
    db.init_app(app)

    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each
    app.logger.info("create_app(): registering blueprints with Flask app object.")
    app.register_blueprint(dataAnalyst, url_prefix="/d")
    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(taker, url_prefix="/t")
    app.register_blueprint(swapper, url_prefix="/s")


    # Don't forget to return the app object
    return app

def setup_logging(app):
    """
    Configure logging for the Flask application in both files and console (Docker Desktop for this project)

    Args:
        app: Flask application instance to configure logging for
    """
    pass

