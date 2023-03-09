from flask import Flask, render_template, request, redirect, session, g
from flask_sqlalchemy import SQLAlchemy
from models import db
from repository import TaskManagerDB

# Initialize Flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'

# Automatically create database tables based on models
task_manager = TaskManagerDB()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method =='POST':
        email = request.form["email"]
        password = request.form["password"]
        
        if task_manager.user_exists(email, password):
            session['email'] = email
            return redirect('/dashboard')
        else:
            error = "Invalid username or password. Please try again."
            return render_template("index.html", message= error)
    return render_template("index.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        task_manager.add_user(request.form["name"], request.form["email"], request.form["password"])
        return redirect('/')
    return render_template("signup.html")

@app.get('/dashboard')
def show_tasks():
    return render_template("dashboard.html")




if __name__ == '__main__':
    app.run(debug = True)
