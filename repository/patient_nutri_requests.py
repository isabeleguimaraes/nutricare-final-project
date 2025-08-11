from helpers import read_all_from_db, write_to_db


# Insert Request to Patient
def insert_pending_request(patient_id, nutri_id, status):
    write_to_db("INSERT INTO patient_nutri_link (patient_id, nutri_id, status) VALUES (?, ?, ?)", (patient_id, nutri_id, status))

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
    
# Reject Request: Deleting Patient-Nutri Link in 'patient_nutri_link' table
def delete_request(patient_id, nutri_id):
    
    write_to_db("DELETE FROM patient_nutri_link WHERE patient_id = ? AND nutri_id = ?", (patient_id, nutri_id))

# Accept Request: Updating Request Status
def update_request_status(patient_id, nutri_id):

    write_to_db("""UPDATE patient_nutri_link SET status = 'Accepted' 
                WHERE patient_id = ? AND nutri_id = ?""", 
                (patient_id, nutri_id))