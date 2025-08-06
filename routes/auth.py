import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import UserMixin, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

# Defining a user: a function that will store the user's data and can be accessed as an object.
class User(UserMixin):
    def __init__(self, id, name, email, hash, role):
        self.id = id
        self.name = name
        self.email = email
        self.hash = hash
        self.role = role



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
        if len(email) < 4:
            errors.append("Email must be at least 4 characters.")

        if len(password) < 6:
            errors.append ("Password must be at least 6 characters.")

        if password != confirmation:
            errors.append("Passwords must match.")
        
        if role not in ['nutritionist', 'patient']:
            errors.append("Invalid Role.")
        
        if not errors:

            # Generate a hash for the password
            hash = generate_password_hash(password)

            # Save users information in users table
            conn = sqlite3.connect('database/nutricare.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email, hash, role) VALUES (?,?,?,?)", (name, email, hash, role))
            conn.commit()

            # Retrieve users data, including user ID
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user_data = cursor.fetchone()
            conn.close()

            # Define Main User based on saved data
            user = User(*user_data)

            # Log In after successful registration and redirect to dashboard
            login_user(user)
            return redirect("/dashboard")

    return render_template("register.html", errors=errors)

# Login Page
@auth_bp.route("/login", methods=['GET', 'POST'])
def login():

    # Initializing variable
    error = None

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        conn = sqlite3.connect('database/nutricare.db')
        cursor = conn.cursor()

        # Retrieve the user information based on email
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user_data = cursor.fetchone()
        conn.close()

        # Verify if user exists and password matches
        if user_data and check_password_hash(user_data[3], password):
            # If everything correct, associate this user with the user in session and log them in
            user = User(*user_data)
            login_user(user)
            
            # Redirect logged in user to dashboard page
            return redirect(url_for('dashboard'))
        else:
            # Error message in html
            error = "Invalid Username or Password."

    return render_template("login.html", error = error)

#Log Out 
@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect("/login")