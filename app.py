from routes.auth import auth_bp, User
import sqlite3
from helpers import check_requests, check_patients, update_request
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

#Create a connection with the database
conn = sqlite3.connect('database/nutricare.db')

#Create a cursor to navigate through the database
cursor = conn.cursor()

#Create a users table (to manage login and id)
cursor.execute(""" CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT,
               email TEXT UNIQUE,
               hash TEXT,  
               role TEXT)
""")

#Create a diet table (to manage relationship between patient and nutritionist and requests)
cursor.execute(""" CREATE TABLE IF NOT EXISTS diet (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER,
               nutri_id INTEGER,
               status TEXT,
               FOREIGN KEY (user_id) REFERENCES users(id),
               FOREIGN KEY (nutri_id) REFERENCES users(id)
               )
               """)

#Create a meals table (to manage patient's diet)
cursor.execute(""" CREATE TABLE IF NOT EXISTS meals (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               diet_id INTEGER,
               meal_type TEXT,
               option TEXT,
               item TEXT,
               FOREIGN KEY (diet_id) REFERENCES diet(id)
               )
               """)


#Commiting the table creation
conn.commit()
#Closing the connection
conn.close()

# Configurinhg the app
app = Flask(__name__)
app.secret_key = "TestPass"

# Configuring Flask Login
login_manager = LoginManager()
# Connecting login manager to the app
login_manager.init_app(app)
# If the user is not logged in, go to (route's function name):
login_manager.login_view = "auth.login"

# Retrieving user ID to start session
@login_manager.user_loader
def load_user(user_id):

    # Connecting to database
    conn = sqlite3.connect('database/nutricare.db')
    cursor = conn.cursor()
    # Selecting user information based on ID
    cursor.execute("SELECT id, name, email, hash, role FROM users where id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    # Return user information to log in user
    if row:
        return User(*row)
    return None

# Registrar blueprints das rotas
app.register_blueprint(auth_bp)


# Defining Conditional Variables to use in HTML (Log in Status)
@app.context_processor
def conditional_flags():
    return {
        'logged_in': current_user.is_authenticated,
        'user': current_user
    }

# ROUTES #

# Home Page
@app.route("/")
def index():
    return render_template("index.html")

# Dashboard Page
@app.route("/dashboard", methods= ["GET", "POST"])
@login_required
def dashboard():

    # Check if there are any linked patients. Their names: show in the sidebar. Their IDs: create a URL for each
    patients = check_patients(current_user.id)
    
    # Check if there are any requests and return names
    requests = check_requests(current_user.id)

    # Redirect to First Patients Page
    if current_user.role == 'nutritionist' and patients and not request.args.get('patient_id'):
        id = patients[0]['id']
        return redirect(url_for('dashboard', patient_id = id))

    if request.method == "POST":

        # Save Data from Form
        action = request.form.get("action")
        nutri_id = request.form.get("nutri_id")
        user_id = current_user.id

        # Update Request Status
        update_request(action, user_id, nutri_id)


        return redirect(url_for('dashboard'))

    return render_template("dashboard.html", patients = patients, requests = requests)
    
# Send Request Page
@app.route("/linking", methods = ['GET', 'POST'])
def linking():
    
    message = ''
    msg_type = ''

    if request.method == "POST":
        email = request.form.get("email")

        conn = sqlite3.connect("database/nutricare.db")
        cursor = conn.cursor()

        # Identifies user ID based on typed email
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()

        # Error message variables to use in HTML
        if result is None:
            message = "This user doesn't exist."
            msg_type = "error"
        
        else:
            # Define user ID
            id = result[0]
            cursor.execute("SELECT user_id FROM diet WHERE user_id = ?", (id,))
            
            # Check if the request has already been sent (Status pending or accepted)
            id_check = cursor.fetchone()
            if id_check:
                message = "You already sent a request to this user"
            
            # If not, add relationship between nutritionist and patient, with pending status.
            else:
                cursor.execute("INSERT INTO diet (user_id, nutri_id, status) VALUES (?, ?, ?)", (id, current_user.id, "Pending"))
                message = "The request was successfully sent to the user."
                msg_type = "success"
                conn.commit()
        conn.close()

    return render_template("linking.html", message = message, msg_type = msg_type)

@app.route("/diet", methods=['GET', 'POST'])
def diet():

    url_patient_id = request.args.get('patient_id')

    if request.method == 'POST':
        conn = sqlite3.connect('database/nutricare.db')
        cursor = conn.cursor()
        nutri_id = current_user.id
        user_id = request.form.get('patient_id')

        cursor.execute("SELECT id FROM diet WHERE nutri_id = ? and user_id = ?", (nutri_id, user_id))
        diet_id = cursor.fetchone()[0]

        meals = ["breakfast", "lunch", "dinner", "snacks"]
        
        for meal in meals:
            for option in range (1,4):
                items = request.form.getlist(f'{meal}_{option}[]')
                for item in items:
                    if item.strip():
                        cursor.execute("""
                            INSERT INTO meals (diet_id, meal_type, option, item) 
                            VALUES (?, ?, ?, ?)  
                            """,
                            (diet_id, meal, option, item))
                        
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard', patient_id=url_patient_id))

    return render_template("diet.html", patient_id = url_patient_id)





# Run App
if __name__ == "__main__":
    app.run(debug=True)