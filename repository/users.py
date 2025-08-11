from helpers import read_all_from_db, read_one_from_db, write_to_db


# Save users information in users table
def save_users_data(name, email, hash, role):

    write_to_db("INSERT INTO users (name, email, hash, role) VALUES (?,?,?,?)", (name, email, hash, role))

# Get users information for log in
def get_user_info_by_email(email):

    user_data = read_one_from_db("SELECT * FROM users WHERE email = ?", (email,))
    if user_data:
        return {"id": user_data[0], "name": user_data[1], "email": user_data[2], "hash": user_data[3], "role": user_data[4]}
    else:
        return None

# Get User Information to Associate with Logged In User
def get_user_info_by_id(user_id):

    user_data = read_one_from_db("SELECT id, name, email, hash, role FROM users where id = ?", (user_id,))
    if user_data:
        return user_data
    else:
        return None