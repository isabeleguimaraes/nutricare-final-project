from helpers import read_all_from_db, read_one_from_db

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
    

def check_if_patient_is_linked(nutri_id, patient_email):

    user_data = read_one_from_db("SELECT users.email FROM users JOIN patient_nutri_link ON users.id = patient_nutri_link.patient_id WHERE nutri_id = ? AND email = ?", (nutri_id, patient_email))
    if user_data:
        return True
    else:
        return None

def find_link_id(nutri_id, patient_id):

    link_id = read_one_from_db("SELECT id FROM patient_nutri_link WHERE nutri_id = ? and patient_id = ?", (nutri_id, patient_id))[0]

    return link_id
