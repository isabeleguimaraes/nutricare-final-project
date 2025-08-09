import sqlite3
from flask import Blueprint, redirect, render_template, url_for, request
from flask_login import current_user
from helpers import update_request_status, delete_request

requests_bp = Blueprint('requests', __name__)


# Patient Response to Request
@requests_bp.route('/respond_request', methods= ['POST'])
def respond_request():

    # Handling Patient's Response to Nutritionist Linking Request

    # Save Data From Form
    action = request.form.get('action')
    nutri_id = request.form.get('nutri_id')
    patient_id = current_user.id

    if action == 'accept':
        update_request_status(patient_id, nutri_id)

    elif action == 'reject':
        delete_request(patient_id, nutri_id)
    
    return redirect(url_for('main.dashboard'))


# Send Request Page
@requests_bp.route("/send_request", methods = ['GET', 'POST'])
def send_request():
    
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
            cursor.execute("SELECT patient_id FROM patient_nutri_link WHERE patient_id = ?", (id,))
            
            # Check if the request has already been sent (Status pending or accepted)
            id_check = cursor.fetchone()
            if id_check:
                message = "You already sent a request to this user"
            
            # If not, add relationship between nutritionist and patient, with pending status.
            else:
                cursor.execute("INSERT INTO patient_nutri_link (patient_id, nutri_id, status) VALUES (?, ?, ?)", (id, current_user.id, "Pending"))
                message = "The request was successfully sent to the user."
                msg_type = "success"
                conn.commit()
        conn.close()

    return render_template("linking.html", message = message, msg_type = msg_type)