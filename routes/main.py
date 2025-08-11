from flask import Blueprint, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from repository.helpers import get_linked_nutris, get_linked_patients, get_pending_requests, get_patient_diet

main_bp = Blueprint('main', __name__)

# Home Page
@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template("index.html")


# Dashboard Page
@main_bp.route("/dashboard", methods = ["GET"])
@login_required
def dashboard():  

    # Initializing Variables
    requests = None
    nutritionists = []
    patients = []
    diet = []

    # Nutritionist Page
    if current_user.role == 'nutritionist':
        
        # Check if there are any linked patients. Their names: show in the sidebar. Their IDs: create a URL for each
        patients = get_linked_patients(current_user.id)

        # Redirect to First Patients Page
        if patients and not request.args.get('patient_id'):
            id = patients[0]['id']
            return redirect(url_for('main.dashboard', patient_id = id, nutri_id = current_user.id, tab='diet'))
        
        
        #Show specific tab
        selected_tab = request.args.get('tab')

        # If there are any associated patients, show their Diet
        if patients:
            try:
                selected_patient_id = int(request.args.get('patient_id'))
            except (ValueError, TypeError):
                selected_patient_id = None
            diet = get_patient_diet(selected_patient_id, current_user.id)
        
      
    # Patients Page

    # Check if there are any requests and return names
    if current_user.role == 'patient':
        
        #Check any pending requests and associated nutritionists
        requests = get_pending_requests(current_user.id)
        nutritionists = get_linked_nutris(current_user.id)
        
    
        # Show first Nutri Page 
        if nutritionists and not request.args.get('nutri_id'):
            id = nutritionists[0]['id']
            return redirect(url_for('main.dashboard', patient_id = current_user.id, nutri_id = id, tab='diet'))
        
        selected_tab = request.args.get('tab')

        if nutritionists:
            try:
                selected_nutri_id = int(request.args.get('nutri_id'))
            except (ValueError, Typeerror):
                selected_nutri_id = None
            diet = get_patient_diet(current_user.id, selected_nutri_id)

    return render_template("dashboard.html", patients = patients, requests = requests, diet = diet, nutritionists = nutritionists, selected_tab = selected_tab)