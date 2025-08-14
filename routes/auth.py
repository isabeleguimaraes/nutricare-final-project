from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import UserMixin, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from repository import save_users_data, get_user_info_by_email

auth_bp = Blueprint('auth', __name__)

   
# Defining a user: a function that will store the user's data and can be accessed as an object.
class User(UserMixin):
    def __init__(self, id, name, email, hash, role):
        self.id = id
        self.name = name
        self.email = email
        self.hash = hash
        self.role = role

# Constants
MIN_PASSWORD_LENGTH = 6
MIN_EMAIL_LENGTH = 4

# Registration Page
@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    
    # Errors list creation to retrieve and show all errors in HTML
    errors = []

    if request.method == 'POST':

        name = request.form.get("name").strip()
        email = request.form.get('email',"").strip()
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        role = request.form.get('role')
      
        # Error Checking
        if len(email) < MIN_EMAIL_LENGTH:
            errors.append("Email must be at least 4 characters.")

        if len(password) < MIN_PASSWORD_LENGTH:
            errors.append ("Password must be at least 6 characters.")

        if password != confirmation:
            errors.append("Passwords must match.")
        
        if role not in ['nutritionist', 'patient']:
            errors.append("Invalid Role.")
        
        if not errors:

            # Generate a hash for the password
            hash = generate_password_hash(password)

            save_users_data(name, email, hash, role)

            # Retrieve users data, including user ID
            user_data = get_user_info_by_email(email)
            # Define Main User based on saved data
            user = User(
                    id=user_data["id"], 
                    name=user_data["name"],
                    email=user_data["email"],
                    hash=user_data["hash"],
                    role=user_data["role"]
                    )

            # Log In after successful registration and redirect to dashboard
            login_user(user)
            return redirect(url_for("main.dashboard"))

    return render_template("register.html", errors=errors)

# Login Page
@auth_bp.route("/login", methods=['GET', 'POST'])
def login():

    # Initializing variable
    error = None

    if request.method == "POST":
        
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            error = "Email and password required."
        else:        
            # Retrieve the user information based on email
            user_data = get_user_info_by_email(email)
            
            # Verify if user exists and password matches
            if user_data and check_password_hash(user_data["hash"], password):
                # If everything correct, associate this user with the user in session and log them in
                user = User(
                        id=user_data["id"], 
                        name=user_data["name"],
                        email=user_data["email"],
                        hash=user_data["hash"],
                        role=user_data["role"]
                        )
                login_user(user)
            
            # Redirect logged in user to dashboard page
                return redirect(url_for('main.dashboard'))
            else:
                # Error message in html
                error = "Invalid Username or Password."

    return render_template("login.html", error = error)

#Log Out 
@auth_bp.route("/logout", methods= ["POST"])
def logout():
    logout_user()
    return redirect(url_for("auth.login"))