import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

# Set up logging for easier debugging
logging.basicConfig(level=logging.DEBUG)

# Create Base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()

# Create the Flask application
app = Flask(__name__)

# Set the secret key from environment variable
app.secret_key = os.environ.get("SESSION_SECRET", "default-dev-secret-key")

# Set up ProxyFix middleware for proper URL generation
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///site.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions with app
db.init_app(app)
login_manager.init_app(app)
csrf.init_app(app)
migrate.init_app(app, db)

# Configure login manager
login_manager.login_view = "login"
login_manager.login_message = "لطفا برای دسترسی به این صفحه وارد شوید."
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# Import routes to register them with the app
with app.app_context():
    try:
        # Import models
        import models
        
        # Create database tables if they don't exist
        db.create_all()
        
        # Import and initialize routes
        from routes import init_routes
        init_routes(app)
        
    except Exception as e:
        logging.error(f"Error during app initialization: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)