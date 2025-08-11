import sqlite3
from flask import Blueprint, redirect, render_template, url_for, request
from flask_login import current_user

from repository import update_request_status, delete_request, get_user_info_by_email, check_if_patient_is_linked, insert_pending_request

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

        patient_email = request.form.get("email")
        nutri_id = current_user.id

        # Identifies user ID based on typed email
        patient_data = get_user_info_by_email(patient_email)

        # Error message variables to use in HTML
        if patient_data is None:
            message = "This user doesn't exist."
            msg_type = "error"
        
        else:
            # Check if the request has already been sent (Status pending or accepted)
            already_linked = check_if_patient_is_linked(nutri_id, patient_email)
            
            if already_linked:
                message = "You already sent a request to this user"
            
            # If not, add relationship between nutritionist and patient, with pending status.
            else:

                insert_pending_request(patient_data["id"], nutri_id, "Pending")
                message = "The request was successfully sent to the user."
                msg_type = "success"
               

    return render_template("linking.html", message = message, msg_type = msg_type)