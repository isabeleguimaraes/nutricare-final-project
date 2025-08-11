# NutriCare Platform

## Video Demo


## Description:
NutriCare is a web platform for nutritionists and patients to create, check and manage diets. 
It's the final project for the CS50 Introduction to Computer Science course.

## Features:
- Nutritionist and patient registration/login
- Nutritionist can send requests to patients
- Patients can accept or reject requests
- Nutritionists can create, edit and share diets
- Nutritionists can remove patient

## Requirements:
The main dependencies are listed in `requirements.txt`:
```
flask
flask-login
werkzeug

```
## Installation
1. Install Python 3.13.5
2. Clone this repository
3. Run: `pip install -r requirements.txt`
4. Create Database `python init_db.py`
4. Start the app: `python app.py`


## Usage
- Access the platform at `http://localhost:5000`
- Register as a nutritionist or patient
- Log in and add a patient
- Patient accepts the request
- Nutritionist Create, edit or remove a diet or item

## Folder Structure
- `app.py`: Main application
- `helpers.py`: Important functions
- `routes/`: Contains route blueprints  
- `static/`: CSS style files
- `templates/`: HTML template files
- `database/`:  SQLITE database files
- `repository/`: Contains transactions functions

## Routes 
- `auth.py` contains routes related to login, logout and registration.
- `app.py` contains routes related to home page, dashboard, diet creation, link patients.

## Future Improvements
- Add Javascript to dynamically add items in diet creation
- Use JSON for diet database
- Implement Dates for each diet to see history
- Include progress tracking and message chat

## TODO
- Error handling
- Improve CSS and HTML tags