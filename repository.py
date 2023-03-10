from sqlalchemy import select, delete, create_engine, inspect, inspect
from sqlalchemy.orm import sessionmaker
from models import *


class TaskManagerDB:
    # set logging=True to log all SQL queries
    def __init__(self, path="sqlite:///activities.db", logging=False):
        self.engine = create_engine(path, echo=logging)
        Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.session = Session()
        
        
    def user_exists(self, email) -> bool:
        
        user = self.session.query(AppUser).filter(AppUser.email == email).first()
        if user:
            return True
        else:
            return False  
    
    def add_user(self, new_user_name, new_user_email, password):
        try:
            self.session.add(AppUser(name=new_user_name, email= new_user_email, password=password ))
            self.session.commit()
            return "Account created Succesfully"
        except:
            return "It seems this email has been used before"
            

    def add_task(self, title, description, user_id):
        self.session.add(Task(title=title, description= description, user_id= user_id ))
        self.session.commit()
    
    
    def get_user(self, user_id_to_lookup):
        result = self.session.get(AppUser, user_id_to_lookup)
        if result == None:
            raise Exception(f"User not Found")
        return result
    
    def get_task(self, task_id_to_lookup):
        result = self.session.get(Task, task_id_to_lookup)
        if result == None:
            raise Exception(f"User not Found")
        return result

    def find_user_by_email(self, email):
        user = self.session.query(AppUser).filter_by(email=email).first()
        return user
    
    def find_tasks_by_user_id(self, user_id):
        tasks = self.session.query(Task).join(AppUser).filter(AppUser.id == user_id).all()
        if len(tasks) == 0:
            return "No tasks yet"
        return tasks
    
    def update_task(self, task_id, new_title, new_description, new_status):
        task = self.session.get(Task, task_id)
        if task is None:
            return {"error": "Task not found"}
        task.title = new_title
        task.description = new_description
        task.status = new_status
        self.session.commit()
        self.session.refresh(task)
        return task

    
    
    def update_user(self, user_id, new_name):
        user = self.session.get(AppUser, user_id)
        if user is None:
            Exception("User  not found")
        user.name = new_name
        self.session.commit()
        self.session.refresh(user)
        return user


    def remove_user(self, user_id_to_remove):
        count = self.session.execute(
            delete(AppUser).where(AppUser.id == user_id_to_remove)
        ).rowcount
        self.session.commit()
        if count == 0:
            raise Exception(f"No user with ID {user_id_to_remove}.")
        
        
    def remove_task(self, task_id_to_remove):
        count = self.session.execute(
            delete(Task).where(Task.id == task_id_to_remove)
        ).rowcount
        self.session.commit()
        if count == 0:
            raise Exception(f"No task with ID {task_id_to_remove}.")

    def get_users (self):
        return self.session.scalars(select(AppUser)).all()

    def search_tasks_by_name(self, task_to_lookup):
        return (
            self.session.query(Task)
            .filter(Task.title.ilike("%" + task_to_lookup + "%"))
            .all()
        )
