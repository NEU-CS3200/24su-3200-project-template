from flask import Flask

from backend.db_connection import db
from backend.users.users_routes import users
from backend.coopPositions.coopPositions_routes import coopPositions
from backend.companyProfiles.companyProfiles_routes import companyProfiles
from backend.workedatpos.workedatpos_routes import workedatpos
from backend.viewsPos.viewsPos_routes import views_position
from backend.applications.applications_routes import applications
from backend.advisoradvisee.advisoradvisee_routes import advisoradvisee
from backend.demographics.demographics_routes import demographics

import os
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)

    # Load environment variables
    # This function reads all the values from inside
    # the .env file (in the parent folder) so they
    # are available in this file.  See the MySQL setup 
    # commands below to see how they're being used.
    load_dotenv()

    # secret key that will be used for securely signing the session 
    # cookie and can be used for any other security related needs by 
    # extensions or your application
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # these are for the DB object to be able to connect to MySQL. 
    app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER').strip()
    app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_ROOT_PASSWORD')
    app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST').strip()
    app.config['MYSQL_DATABASE_PORT'] = int(os.getenv('DB_PORT').strip())
    app.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME').strip()

    # Initialize the database object with the settings above. 
    app.logger.info('current_app(): starting the database connection')
    db.init_app(app)

    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each
    app.logger.info('current_app(): registering blueprints with Flask app object.')   
    app.register_blueprint(users)
    app.register_blueprint(coopPositions)
    app.register_blueprint(companyProfiles)
    app.register_blueprint(workedatpos)
    app.register_blueprint(views_position)
    app.register_blueprint(applications)
    app.register_blueprint(advisoradvisee)
    app.register_blueprint(demographics)

    # Don't forget to return the app object
    return app

