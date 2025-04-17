import logging
logging.basicConfig(level=logging.DEBUG)

from flask import Flask
from db_connection import db
from users.users_routes import users
from stores.stores_routes import stores
from clubs.club_routes import clubs
from colleges.colleges_routes import colleges
from admin.admin_routes import admin
from discounts.discount_routes import discounts
from savedDiscounts.savedDiscounts_routes import savedDiscounts

import os
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER')
    app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_ROOT_PASSWORD')
    app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST')
    app.config['MYSQL_DATABASE_PORT'] = int(os.getenv('DB_PORT'))
    app.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME')

    db.init_app(app)

    @app.route("/")
    def welcome():
        return "<h1>Welcome to the CampusPerks Backend</h1>"

    app.register_blueprint(users, url_prefix='/u')
    app.register_blueprint(stores, url_prefix='/s')
    app.register_blueprint(colleges, url_prefix='/col')
    app.register_blueprint(admin, url_prefix='/a')
    app.register_blueprint(discounts, url_prefix='/d')
    app.register_blueprint(savedDiscounts, url_prefix='/sd')
    app.register_blueprint(clubs, url_prefix='/cl')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=4000)