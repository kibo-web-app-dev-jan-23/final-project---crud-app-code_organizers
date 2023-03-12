from flask import Flask, render_template, redirect, url_for, request, session, flash
from repository import *
from werkzeug.security import check_password_hash, generate_password_hash
from models import Status

app = Flask(__name__)
app.secret_key = 'OjosAppDivineTracks'

db = TaskManagerDB("sqlite:///activities.db", True)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = db.find_user_by_email(email)
        if db.user_exists(email) and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST', 'DELETE'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if db.user_exists(email):
            flash('This email is already linked to an account', 'error')
            return redirect(url_for('signup'))
        else:
            hashed_password = generate_password_hash(password)
            db.add_user(name, email, hashed_password)
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
    else:
        return render_template('signup.html')

@app.route('/dashboard', methods=['POST','GET', 'DELETE'])
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = db.get_user(user_id)
        
        tasks = db.find_tasks_by_user_id(user_id)
        
        return render_template('dashboard.html', user=user, tasks=tasks)
    else:
        return redirect(url_for('login'))

@app.route('/tasks/<int:task_id>', methods=['POST','GET'])
def view_task(task_id):
    if request.method == 'POST':    
        
        new_title = request.form['title']
        new_description = request.form['description']
        new_status = request.form['status']
        breakpoint()
        db.update_task(task_id, new_title, new_description, new_status)
        
        return redirect(url_for('dashboard'))
    else:
        task = db.get_task(task_id)
        return render_template('task_details.html', task=task, Status=Status)
 
@app.route('/change-status/<int:task_id>', methods=['POST'])
def update_status(task_id):
    task = db.get_task(task_id)
    new_status = request.form['status']
    updated_task = db.update_task(task_id, task.title, task.description, new_status)

    return render_template('task_details.html', task=updated_task, Status=Status)
 
@app.route('/add_task', methods=['POST'])
def add_task(): 
    title = request.form['title']
    description = request.form['description']
    user_id = session.get('user_id')
    
    db.add_task(title, description, user_id)
    return redirect(url_for('dashboard')) 


@app.route('/delete-task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    db.remove_task(task_id)
    message = {"message": f"Task{task_id} deleted successfully"}, 201
    return redirect(url_for("index"))
    
@app.route('/delete-account', methods=['DELETE'])
def delete_user():
    user_id = session.get('user_id')
    db.remove_user(user_id)
    session.pop('user_id', None)
    return redirect(url_for('signup'))


@app.post('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug = True)

