import os
from flask import Flask
from init import db, ma, bcrypt, jwt
from flask_jwt_extended import JWTManager

# Import Blueprints
from controllers.theater_controller import theater_bp
from controllers.movie_controller import movie_bp
from controllers.customer_controller import customer_bp
from controllers.employee_controller import employee_bp
from controllers.invoice_controller import invoice_bp
from controllers.showtime_controller import showtime_bp
from controllers.ticket_controller import ticket_bp
from controllers.cli_controller import db_commands
from controllers.auth_controller import auth_bp

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "default_secret_key")

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register Blueprints
    app.register_blueprint(db_commands)
    # app.register_blueprint(auth_bp)
    app.register_blueprint(theater_bp)
    app.register_blueprint(movie_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(invoice_bp)
    app.register_blueprint(showtime_bp)
    app.register_blueprint(ticket_bp)

    return app
