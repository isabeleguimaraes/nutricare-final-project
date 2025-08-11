import sqlite3
from flask import Blueprint, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from repository.helpers import get_linked_nutris, get_linked_patients, get_pending_requests, get_patient_diet, delete_current_diet, save_new_diet

management_bp = Blueprint('management', __name__)


# Creating and Editing a Diet
@management_bp.route("/manage_diet", methods=['GET', 'POST'])
def manage_diet():

    url_patient_id = request.args.get('patient_id') 
    patient_diet = get_patient_diet(url_patient_id, current_user.id)
    meals = ["breakfast", "lunch", "dinner", "snacks"]

    if request.method == 'POST':

        nutri_id = current_user.id
        patient_id = request.form.get('patient_id')

        delete_current_diet(nutri_id, patient_id)

        for meal in meals:
            for combination in range (1,4):
                items = request.form.getlist(f'{meal}_{combination}[]')
                for item in items:
                    if item.strip():
                        save_new_diet(nutri_id, patient_id, meal, combination, item)
                        
        return redirect(url_for('main.dashboard', patient_id=url_patient_id,))

    return render_template("diet.html", patient_id = url_patient_id, diet = patient_diet, meals=meals)