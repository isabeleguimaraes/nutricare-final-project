import sqlite3

# DATABASE INTERACTION

DB_NAME = 'database/nutricare.db'

# Insert, Delete, Update
def write_to_db(query, params=()):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

# Select All Information
def read_all_from_db(query, params=()):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()

    return result

# Select One Information
def read_one_from_db(query, params=()):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchone()
    conn.close()

    return result


# HELPERS FUNCTIONS

# Save users information in users table
def save_users_data(name, email, hash, role):

    write_to_db("INSERT INTO users (name, email, hash, role) VALUES (?,?,?,?)", (name, email, hash, role))

# Get users information for log in
def get_user_info_by_email(email):

    user_data = read_one_from_db("SELECT * FROM users WHERE email = ?", (email,))

    return {"id": user_data[0], "name": user_data[1], "email": user_data[2], "hash": user_data[3], "role": user_data[4]}

# Get User Information to Associate with Logged In User
def get_user_info_by_id(user_id):

    user_data = read_one_from_db("SELECT id, name, email, hash, role FROM users where id = ?", (user_id,))

    return user_data

# Check Pending Requests for Patients
def get_pending_requests(patient_id):

    results = read_all_from_db("""
                   SELECT users.id, users.name FROM users 
                   JOIN patient_nutri_link ON users.id = patient_nutri_link.nutri_id 
                   WHERE patient_nutri_link.patient_id = ? AND patient_nutri_link.status = 'Pending'""", 
                   (patient_id,))

    # Return Dictionary of Requests (Name and ID) or Empty List
    if results:
        return [{"id": result[0], "name": result[1]} for result in results]
    else:
        return []

# Get Patients Linked to Nutritionist
def get_linked_patients(nutri_id):

    # Query to Show Patients that Accepted the Nutri's Request
    patients = read_all_from_db("""SELECT users.id AS patient_id, users.name AS patient_name 
                   FROM users 
                   JOIN patient_nutri_link ON users.id = patient_nutri_link.patient_id 
                   WHERE nutri_id = ? AND patient_nutri_link.status = 'Accepted'""", 
                   (nutri_id,))

    # Return Dictionary of Patients (Name and ID) or Empty List  
    return [{"id": patient[0], "name": patient[1]} for patient in patients]

    
# Get Nutritionists Linked to Patient
def get_linked_nutris(patient_id):

    nutritionists = read_all_from_db("""SELECT users.id AS nutri_id, users.name AS nutri_name 
                        FROM users 
                        JOIN patient_nutri_link ON users.id = patient_nutri_link.nutri_id 
                        WHERE patient_nutri_link.patient_id = ? AND status = 'Accepted' """, 
                        (patient_id,))
    
    # Return Dictionary of Nutritionists (Name and ID) or Empty List  
    return [{"id": nutri[0], "name": nutri[1]} for nutri in nutritionists]
    

# Rejected: Deleting Request Status
def delete_request(patient_id, nutri_id):
    
    # Delete Nutritionist-Patient Connection in 'patient_nutri_link' Table
    write_to_db("DELETE FROM patient_nutri_link WHERE patient_id = ? AND nutri_id = ?", (patient_id, nutri_id))

# Accepted: Updating Request Status
def update_request_status(patient_id, nutri_id):

    # Accepted: Change Status
    write_to_db("""UPDATE patient_nutri_link SET status = 'Accepted' 
                WHERE patient_id = ? AND nutri_id = ?""", 
                (patient_id, nutri_id))


def get_patient_diet(patient_id, nutri_id):

     # Find Patient patient_nutri_link Data
    results = read_all_from_db("""
                    SELECT meal_type, combination, item 
                    FROM diet
                    JOIN patient_nutri_link ON diet.link_id = patient_nutri_link.id
                    WHERE patient_nutri_link.patient_id = ? AND patient_nutri_link.nutri_id = ?
                """, (patient_id, nutri_id))

    return [{"meal_type": result[0], "combination": result[1], "item": result[2]} for result in results]

def find_link_id(nutri_id, patient_id):

    link_id = read_one_from_db("SELECT id FROM patient_nutri_link WHERE nutri_id = ? and patient_id = ?", (nutri_id, patient_id))[0]

    return link_id

def delete_current_diet(nutri_id, patient_id,):

    link_id = find_link_id(nutri_id, patient_id)

    # Deleting Data
    write_to_db("DELETE FROM diet WHERE link_id = ?", (link_id,))

def save_new_diet(nutri_id, patient_id, meal, combination, item):
    
    link_id = find_link_id(nutri_id, patient_id)
    write_to_db("""
                INSERT INTO diet (link_id, meal_type, combination, item) 
                VALUES (?, ?, ?, ?)  
                """,
                (link_id, meal, combination, item))

def check_if_patient_is_linked(nutri_id, patient_email):

    user_data = read_one_from_db("SELECT email, id FROM users JOIN patient_nutri_link ON users.id = patient_nutri_link.patient_id WHERE nutri_id = ? AND email = ?", (nutri_id, patient_email))

    return {"email": user_data[0], "id": user_data[1]}

def insert_pending_request(patient_id, nutri_id, status):
    write_to_db("INSERT INTO patient_nutri_link (patient_id, nutri_id, status) VALUES (?, ?, ?)", (patient_id, nutri_id, status))