# NutriCare Platform

## Video Demo


## Description:
NutriCare is a web platform for nutritionists and patients to manage diets, track progress, and communicate via messages and comments.

## Features:
- Nutritionist and patient registration/login
- Nutritionist can add patients
- Diet management and meal tracking
- Progress visualization
- Messaging and comments between users

## Requirements:
The main dependencies are listed in `requirements.txt`:
```
flask
flask-login
werkzeug
sqlite3

```
## Installation
1. Install Python 3.13.5
2. Clone this repository
3. Run: `pip install -r requirements.txt`
4. Start the app: `python app.py`

## Usage
- Access the platform at `http://localhost:5000`
- Register as a nutritionist or patient
- Log in and add a patient
- Create, edit or remove a diet or item

## Folder Structure
- `app.py`: Main application
- `helpers.py`: Important functions
- `routes/`: Contains route blueprints  
- `static/`: CSS style files
- `templates/`: HTML template files
- `database/`:  SQLITE database files

## Routes 
- `auth.py` contains routes related to login, logout and registration.
- `app.py` contains routes related to home page, dashboard, diet creation, link patients.

## Future Improvements
- Add Javascript to dynamically add items in diet creation
- Use JSON for diet database
- Implement Dates for each diet to see history

## TODO
- Home Page (index)
- Show diet in user's dashboard
- Add progress charts and information
- Add message system
- Error handling
- Improve CSS and HTML tags
- Create a separate folder for table creation