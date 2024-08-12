import logging

logging.basicConfig(level=logging.DEBUG)

import atexit
import os
from dotenv import load_dotenv
from flask import Flask

from backend.db_connection import init_db, cleanup_db
from backend.customers.customer_routes import customers
from backend.preferences.preference_routes import preferences


def create_app():
    app = Flask(__name__)

    # Load environment variables
    load_dotenv()

    # secret key that will be used for securely signing the session
    # cookie and can be used for any other security related needs by
    # extensions or your application
    # app.config['SECRET_KEY'] = 'someCrazyS3cR3T!Key.!'
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    init_db(
        os.getenv("DB_HOST"),
        int(os.getenv("DB_PORT")),
        os.getenv("DB_USER"),
        os.getenv("MYSQL_ROOT_PASSWORD"),
        os.getenv("DB_NAME"),
    )

    def close_db():
        app.logger.info("Server stopping, closing db")
        cleanup_db()

    atexit.register(close_db)

    app.logger.info("current_app(): registering blueprints with Flask app object.")

    app.register_blueprint(customers)
    app.register_blueprint(preferences)

    # Don't forget to return the app object
    return app
