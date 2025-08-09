import sqlite3
from flask import Blueprint, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from helpers import get_linked_nutris, get_linked_patients, get_pending_requests, get_patient_diet

management_bp = Blueprint('management', __name__)


# Creating and Editing a Diet
@management_bp.route("/manage_diet", methods=['GET', 'POST'])
def manage_diet():

    url_patient_id = request.args.get('patient_id') 
    patient_diet = get_patient_diet(url_patient_id, current_user.id)
    meals = ["breakfast", "lunch", "dinner", "snacks"]

    if request.method == 'POST':
        conn = sqlite3.connect('database/nutricare.db')
        cursor = conn.cursor()
        nutri_id = current_user.id
        patient_id = request.form.get('patient_id')

        cursor.execute("SELECT id FROM patient_nutri_link WHERE nutri_id = ? and patient_id = ?", (nutri_id, patient_id))
        link_id = cursor.fetchone()[0]

        cursor.execute("DELETE FROM diet WHERE link_id = ?", (link_id,))
        for meal in meals:
            for combination in range (1,4):
                items = request.form.getlist(f'{meal}_{combination}[]')
                for item in items:
                    if item.strip():
                        cursor.execute("""
                            INSERT INTO diet (link_id, meal_type, combination, item) 
                            VALUES (?, ?, ?, ?)  
                            """,
                            (link_id, meal, combination, item))
                        
        conn.commit()
        conn.close()
        return redirect(url_for('main.dashboard', patient_id=url_patient_id,))

    return render_template("diet.html", patient_id = url_patient_id, diet = patient_diet, meals=meals)