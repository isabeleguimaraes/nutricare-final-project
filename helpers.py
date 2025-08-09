import sqlite3


# Get User Information to Associate with Logged In User
def get_user_info_by_id(user_id):

    # Connecting to database
    conn = sqlite3.connect('database/nutricare.db')
    cursor = conn.cursor()
    # Selecting user information based on ID
    cursor.execute("SELECT id, name, email, hash, role FROM users where id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    return row

# Check Pending Requests for Patients
def get_pending_requests(patient_id):

    # Open Connection
    conn = sqlite3.connect('database/nutricare.db')
    cursor = conn.cursor()

    # Query to Select Pending Requests
    cursor.execute("""
                   SELECT users.id, users.name FROM users 
                   JOIN patient_nutri_link ON users.id = patient_nutri_link.nutri_id 
                   WHERE patient_nutri_link.patient_id = ? AND patient_nutri_link.status = 'Pending'""", 
                   (patient_id,))
    results = cursor.fetchall()
    conn.close()

    # Return Dictionary of Requests (Name and ID) or Empty List
    if results:
        return [{"id": result[0], "name": result[1]} for result in results]
    else:
        return []

# Get Patients Linked to Nutritionist
def get_linked_patients(nutri_id):

    # Open Connection
    conn = sqlite3.connect("database/nutricare.db")
    cursor = conn.cursor()

    # Query to Show Patients that Accepted the Nutri's Request
    cursor.execute("""SELECT users.id AS patient_id, users.name AS patient_name 
                   FROM users 
                   JOIN patient_nutri_link ON users.id = patient_nutri_link.patient_id 
                   WHERE nutri_id = ? AND patient_nutri_link.status = 'Accepted'""", 
                   (nutri_id,))
    patients = cursor.fetchall()
    conn.close()

    # Return Dictionary of Patients (Name and ID) or Empty List  
    return [{"id": patient[0], "name": patient[1]} for patient in patients]

    
# Get Nutritionists Linked to Patient
def get_linked_nutris(patient_id):

    # Open Connection
    conn = sqlite3.connect('database/nutricare.db')
    cursor = conn.cursor()

    # Query for Nutritionists ID
    cursor.execute("""SELECT users.id AS nutri_id, users.name AS nutri_name 
                   FROM users 
                   JOIN patient_nutri_link ON users.id = patient_nutri_link.nutri_id 
                   WHERE patient_nutri_link.patient_id = ? AND status = 'Accepted' """, 
                   (patient_id,))
    nutritionists = cursor.fetchall()

    # Return Dictionary of Nutritionists (Name and ID) or Empty List  
    return [{"id": nutri[0], "name": nutri[1]} for nutri in nutritionists]
    

# Rejected: Deleting Request Status
def delete_request(patient_id, nutri_id):

    # Open Connection
    conn = sqlite3.connect('database/nutricare.db')
    cursor = conn.cursor()

    # Delete Nutritionist-Patient Connection in 'patient_nutri_link' Table
    cursor.execute("DELETE FROM patient_nutri_link WHERE patient_id = ? AND nutri_id = ?", (patient_id, nutri_id))
    conn.commit()
        
    conn.close()

# Accepted: Updating Request Status
def update_request_status(patient_id, nutri_id):

    # Open Connection
    conn = sqlite3.connect('database/nutricare.db')
    cursor = conn.cursor()

    # Accepted: Change Status
    cursor.execute("UPDATE patient_nutri_link SET status = 'Accepted' WHERE patient_id = ? AND nutri_id = ?", (patient_id, nutri_id))
    conn.commit()
        
    conn.close()


def get_patient_diet(patient_id, nutri_id):

    # Open Connection
    conn = sqlite3.connect('database/nutricare.db')
    cursor = conn.cursor()

    # Find Patient patient_nutri_link Data
    cursor.execute("""
                    SELECT meal_type, combination, item 
                    FROM diet
                    JOIN patient_nutri_link ON diet.link_id = patient_nutri_link.id
                    WHERE patient_nutri_link.patient_id = ? AND patient_nutri_link.nutri_id = ?
                """, (patient_id, nutri_id))
    results = cursor.fetchall()
    conn.close()

    return [{"meal_type": result[0], "combination": result[1], "item": result[2]} for result in results]