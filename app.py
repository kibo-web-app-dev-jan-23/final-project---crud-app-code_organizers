from flask import Flask, render_template, redirect, url_for, request, session, flash
from repository import TaskManagerDB
from werkzeug.security import check_password_hash, generate_password_hash

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

@app.route('/signup', methods=['GET', 'POST'])
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

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = db.get_user(user_id)
        tasks = db.find_tasks_by_user_id(user_id)
        return render_template('dashboard.html', user=user, tasks=tasks)
    else:
        return redirect(url_for('login'))

@app.route('/tasks/<int:task_id>', methods=['PUT','GET', 'DELETE'])
def view_task(task_id):
    if request.method == 'PUT':    
        data = request.get_json()
        new_title = data['title']
        new_description = data['description']
        new_status = data['status']
        db.update_task(task_id, new_title, new_description, new_status)
        return redirect(url_for('dashboard'))
    task = db.get_task(task_id)
    return render_template('task.html', task )    
    


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    db.remove_task(task_id)
    message = {"message": "Task deleted successfully"}, 201
    return redirect(url_for('dashboard'))
    
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db.remove_user(user_id)
    return redirect(url_for('signup'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))



if __name__ == '__main__':
    db.initialize_db_schema()
    app.run(debug=True)
