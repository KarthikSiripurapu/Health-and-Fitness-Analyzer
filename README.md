# Health-and-Fitness-Analyzer

This is a Python web app that helps you track your fitness data over multiple days. You can input your daily:
* Steps walked
* Calories burned
* Sleep hours
* Weight
This app then shows you averages and creates a progress chart.

# How to Run -
Install requirements:
pip install -r requirements.txt

Run the application:
uvicorn main:app --reload

# How to Use
Start: Enter your name and how many days you want to track

Daily Input: Each day, enter your steps, calories, sleep, and weight

Results: After all days, see your averages and a progress chart

# Technology Used
FastAPI - Web framework
SQLite - Database
Pandas & NumPy - Data calculations
Matplotlib - Charts and graphs
Jinja2 - HTML templates
