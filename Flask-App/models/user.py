from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    def __init__(self, data):
        self.id = data['id']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.animals = []

        #  validates register / login
    @staticmethod
    def validate_user(user):
        is_valid = True
# Name validation 
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters")
            is_valid = False
# Email validation
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False
        if User.get_user_by_email(user['email']):
            flash('That email is already in use')
            is_valid = False
# Password validation
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid = False
        if user['password'] != user['con_password']:
            flash("Passwords do not match")
            is_valid = False
        return is_valid

    @staticmethod
    def login(data):
        this_user = User.get_user_by_email(data['email'])
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['user_id'] = this_user.id
                session['user_name'] = f'{this_user.first_name} {this_user.last_name}'
                return True
        flash("Your login email or password was wrong.")
        return False

#  Saves data to db
    @classmethod
    def create_user(cls, user_info):
        if not cls.validate_user(user_info):
            return False
        user_info = cls.run_user_data(user_info)
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        ;"""
        user_id = connectToMySQL('tv_shows').query_db(query, user_info)
        session['user_id'] = user_id
        session['user_name'] = f'{user_info["first_name"]} {user_info["last_name"]}'
        return user_id
    
    @classmethod
    def get_user_by_email(cls, email):
        data = {'email': email}
        query = """
        SELECT *
        FROM users
        WHERE email = %(email)s;"""
        user_data = connectToMySQL('tv_shows').query_db(query, data)
        if user_data:
            return cls(user_data[0])
        return False
    
    @staticmethod
    def run_user_data(data):
        run_data = {
            'email': data['email'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'password': bcrypt.generate_password_hash(data['password'])
        }
        print('!?!?!?!?!?!?', run_data)
        return(run_data)