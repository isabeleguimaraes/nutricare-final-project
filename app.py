from routes.auth import auth_bp, User
from routes.main import main_bp
from routes.requests import requests_bp
from routes.management import management_bp

import sqlite3
from helpers import get_pending_requests, get_linked_patients, update_request_status, delete_request, get_patient_diet, get_linked_nutris, get_user_info_by_id
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, current_user

# Configuring the app
app = Flask(__name__)
app.secret_key = "TestPass"

# Configuring Flask Login
login_manager = LoginManager()
# Connecting login manager to the app
login_manager.init_app(app)
# If the user is not logged in, go to (route's function name):
login_manager.login_view = "auth.login"

# Retrieving user information and creating a 'User'.
@login_manager.user_loader
def load_user(user_id):

    # Get User Information
    info = get_user_info_by_id(user_id)
    # Return user information to log in user
    if info:
        return User(*info)
    return None

# Register Route Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(requests_bp)
app.register_blueprint(management_bp)


# Defining Conditional Variables to use in HTML (Log in Status)
@app.context_processor
def conditional_flags():
    return {
        'logged_in': current_user.is_authenticated,
        'user': current_user
    }

# Run App
if __name__ == "__main__":
    app.run(debug=True)