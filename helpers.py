import sqlite3

# Check Pending Requests for Patients
def check_requests(user_id):

    # Open Connection
    conn = sqlite3.connect('database/nutricare.db')
    cursor = conn.cursor()

    # Query to Select Pending Requests
    cursor.execute("""
                   SELECT users.id, users.name FROM users 
                   JOIN diet ON users.id = diet.nutri_id 
                   WHERE diet.user_id = ? AND diet.status = 'Pending'""", 
                   (user_id,))
    results = cursor.fetchall()
    conn.close()

    # Return Dictionary of Requests (Name and ID) or Empty List
    if results:
        return [{"id": result[0], "name": result[1]} for result in results]
    else:
        return []

# Check Patients List for Nutritionists
def check_patients(user_id):

    # Open Connection
    conn = sqlite3.connect("database/nutricare.db")
    cursor = conn.cursor()

    # Query to Show Patients that Accepted the Nutri's Request
    cursor.execute("SELECT users.id, users.name FROM users JOIN diet ON users.id = diet.user_id WHERE nutri_id = ? AND diet.status = 'Accepted'", (user_id,))
    patients = cursor.fetchall()
    conn.close()

    # Return Dictionary of Patients (Name and ID) or Empty List
    if patients:
        return [{"id": patient[0], "name": patient[1]} for patient in patients]
    else:
        return []
    
# Check Nutritionists Available
def check_nutri(user_id):

    # Open Connection
    conn = sqlite3.connect('database/nutricare.db')
    cursor = conn.cursor()

    # Query for Nutritionists ID
    cursor.execute("""SELECT users.id, users.name 
                   FROM users 
                   JOIN diet ON users.id = diet.nutri_id 
                   WHERE diet.user_id = ? AND status = 'Accepted' """, 
                   (user_id,))
    nutritionists = cursor.fetchall()

    if nutritionists:
        return [{"id": nutri[0], "name": nutri[1]} for nutri in nutritionists]
    else:
        return []

# Updating Request Status
def update_request(action, user, nutri):

    # Open Connection
    conn = sqlite3.connect('database/nutricare.db')
    cursor = conn.cursor()

    # Accepted: Change Status
    if action == "accept": 
        cursor.execute("UPDATE diet SET status = 'Accepted' WHERE user_id = ? AND nutri_id = ?", (user, nutri))
        conn.commit()
        
    # Rejected: Delete Request
    elif action == "reject":
        cursor.execute("DELETE FROM diet WHERE user_id = ? AND nutri_id = ?", (user, nutri))
        conn.commit()
        
    conn.close()

# 

def patient_diet(user_id, nutri_id):

    # Open Connection
    conn = sqlite3.connect('database/nutricare.db')
    cursor = conn.cursor()

    # Find Patient Diet Data
    cursor.execute("""
                    SELECT meal_type, option, item 
                    FROM meals 
                    JOIN diet ON meals.diet_id = diet.id
                    WHERE diet.user_id = ? AND diet.nutri_id = ?
                """, (user_id, nutri_id))
    results = cursor.fetchall()
    conn.close()

    return [{"meal_type": result[0], "option": result[1], "item": result[2]} for result in results]