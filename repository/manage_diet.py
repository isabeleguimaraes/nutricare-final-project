from helpers import read_all_from_db, write_to_db
from .patient_nutri_link import find_link_id

# Return Patient's Diet Based on Nutritionist
def get_patient_diet(patient_id, nutri_id):

     # Find Patient patient_nutri_link Data
    results = read_all_from_db("""
                    SELECT meal_type, combination, item 
                    FROM diet
                    JOIN patient_nutri_link ON diet.link_id = patient_nutri_link.id
                    WHERE patient_nutri_link.patient_id = ? AND patient_nutri_link.nutri_id = ?
                """, (patient_id, nutri_id))

    return [{"meal_type": result[0], "combination": result[1], "item": result[2]} for result in results]


# Delete Diet from Database
def delete_current_diet(nutri_id, patient_id,):

    link_id = find_link_id(nutri_id, patient_id)

    # Deleting Data
    write_to_db("DELETE FROM diet WHERE link_id = ?", (link_id,))

# Insert new diet in Database
def save_new_diet(nutri_id, patient_id, meal, combination, item):
    
    link_id = find_link_id(nutri_id, patient_id)
    write_to_db("""
                INSERT INTO diet (link_id, meal_type, combination, item) 
                VALUES (?, ?, ?, ?)  
                """,
                (link_id, meal, combination, item))
