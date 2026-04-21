from flask import Flask
from dotenv import load_dotenv
import os
import logging

from backend.db_connection import init_app as init_db
from backend.audiovate_routes.payoutProfiles.payout_routes import payout_profiles
from backend.audiovate_routes.assets.asset_routes import assets
from backend.audiovate_routes.artists.artist_routes import artists
from backend.audiovate_routes.users.user_routes import users
from backend.audiovate_routes.releases.release_routes import releases
from backend.audiovate_routes.systemLogs.systemLog_routes import system_logs
from backend.audiovate_routes.helpRequests.helpRequest_routes import help_requests


def create_app():
    app = Flask(__name__)

    app.logger.setLevel(logging.DEBUG)
    app.logger.info('API startup')

    # Load environment variables from the .env file so they are
    # accessible via os.getenv() below.
    load_dotenv()

    # Secret key used by Flask for securely signing session cookies.
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # Database connection settings — values come from the .env file.
    app.config["MYSQL_DATABASE_USER"] = os.getenv("DB_USER").strip()
    app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("MYSQL_ROOT_PASSWORD").strip()
    app.config["MYSQL_DATABASE_HOST"] = os.getenv("DB_HOST").strip()
    app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("DB_PORT").strip())
    app.config["MYSQL_DATABASE_DB"] = os.getenv("DB_NAME", "Audiovate").strip()

    # Register the cleanup hook for the database connection.
    app.logger.info("create_app(): initializing database connection")
    try:
        init_db(app)
    except Exception as e:
        app.logger.error(f"Database initialization failed: {e}")

    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each.
    app.logger.info("create_app(): registering blueprints")
    app.register_blueprint(payout_profiles, url_prefix="/payoutProfiles")
    app.register_blueprint(assets, url_prefix="/assets")
    app.register_blueprint(artists, url_prefix="/artists")
    app.register_blueprint(users, url_prefix="/users")
    app.register_blueprint(releases)
    app.register_blueprint(system_logs)
    app.register_blueprint(help_requests)


    return app