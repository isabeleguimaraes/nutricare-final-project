# NutriCare Platform

## Video Demo


## Description:
NutriCare is a web platform designed for nutritionists and patients to create, manage, and share personalized diets. This project was developed as the final assignment for Harvard's CS50x: Introduction to Computer Science.

## Tech Stack
| Technology       | Description |
|------------------|-------------|
| **Python**       | Main programming language used for backend logic |
| **Flask**        | Lightweight web framework for routing and server-side functionality |
| **SQLite**       | Relational database used to store user and diet data locally |
| **Jinja2**       | Template engine for rendering dynamic HTML pages |
| **Flask-Login**  | User session and authentication management |
| **Werkzeug**     | Utilities for password hashing and request handling |
| **HTML/CSS**     | Structure and styling of the web pages |

## Features:
- User registration and login for both nutritionists and patients  
- Nutritionists can send connection requests to patients  
- Patients can accept or reject requests  
- Nutritionists can create, edit, and share diets  
- Nutritionists can remove linked patients  

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
4. Initialize Database `python init_db.py`
4. Start the app: `python app.py`


## Usage
- Open `http://localhost:5000` in your browser  
- Register as a nutritionist or patient  
- Nutritionists can send requests to patients  
- Patients accept or reject requests  
- Nutritionists manage diets: create, edit, or delete items  

## Folder Structure
| File/Folder   | Description                |
| ------------- | -------------              |
| `app.py`      | Main application file      |
| `helpers.py`  | Utility functions          |
| `init_db.py`  | Database initialization    |
| `routes/`     | Flask route blueprints     |
| `static/`     | CSS styles and images      |
| `templates/`  | HTML templates             |
| `database/`   | SQLite database files      |
| `repository/`  | Database transaction logic |

## Routes Overview
- `auth.py` Login, logout, and registration
- `main.py` Dashboard and index routes
- `management.py` Diet management routes
- `requests.py` Patient-nutritionist request handling

## Static
- `/css/` Page-specific stylesheets
- `/images/` App images

## Templates
- `base.html` Shared layout for all pages
- `dashboard.html` Main interface for users
- `diet.html` Diet creation/editing page
- `login.html` Login form
- `register.html` Registration form
- `send_request.html` Request form for nutritionists
- `partials/dashboard_sidebar.html` Dashboard Sidebar with conditionals

## Database
- `nutricare.db` SQLite database file

## Repository 
- `manage_diet.py` Handle diet access, creation and deletion
- `patient_nutri_link.py` Manage linked users
- `patient_nutri_requests.py` Handle pending requests
- `users.py` User data access and updates

## Future Improvements
- Add JavaScript for dynamic diet item creation
- Improve UX with confirmation dialogs and feedback
- Use JSON for diet storage
- Implement date tracking for diet history
- Add progress tracking and messaging system

## Challenges and Learning
- As this was my first web app creation, I encountered many challenges along the way. One of them was figuring out how to organize my files as the project grew. I realized how important clear naming is, helping make each file’s purpose obvious. Also, grouping related themes and functions together made everything easier to navigate.
- Another challenge was learning how to use URL parameters to create dynamic pages. That opened up a lot of possibilities: I was able to generate unique pages for each patient and their diet, and clearly link each function to the right patient and nutritionist.
- Creating and manipulating database tables was very important for my learning process. Understanding how users input data and how that data gets stored helped me build more organized and functional features. Even though the diet creation process was simple, I’m proud that I got it working and could use the related tables to pull the right information.
- Structuring HTML with Jinja was super helpful. Learning when and how to use variables and conditionals made it much easier to build pages that adapt to different user types.


## Reflections
- As I went through the CS50x course, I built a solid foundation from the exercises and lectures. However, I feel that by actually making my first web app is when I learned the most. It gave me a chance to apply what I learned in class and turn that knowledge into something real and functional.
- I worked on the project a little bit every day, and each step taught me something new. I spent time researching, asking questions to people with more experience, and using tools like ChatGPT to help me understand concepts better (not just to get answers, but to actually learn). That process helped me grow in both backend and frontend development.
- While building the app, I realized there are many new features I could add and ways to improve it. That made me excited to keep learning and refining my skills with each new project.