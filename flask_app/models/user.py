from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    db = 'wildlife_schema'
    def __init__(self, data):
        self.id = data['id']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.email = data['email']
        self.password = data['password']
        self.createdAt = data['createdAt']
        self.updateAt = data['updateAt']
        self.animals = []

        def fullName(self):
            return f'{self.firstName} {self.lastName}'

        #  validates register / login
    @staticmethod
    def validate_user(user):
        is_valid = True
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(User.db).query_db(query, user)
# Name validation 
        if len(user['firstName']) < 2:
            is_valid = False
            flash("First name must be at least 2 characters")
        if len(user['lastName']) < 2:
            is_valid = False
            flash("Last name must be at least 2 characters")
# Email validation
        if not EMAIL_REGEX.match(user['email']):
            is_valid = False
            flash("Invalid email address!")
        if len(results) >= 1:
            is_valid = False
            flash('That email is already in use')
# Password validation
        if len(user['password']) < 8:
            is_valid = False
            flash("Password must be at least 8 characters")
        if user['password'] != user['con_password']:
            is_valid = False
            flash("Passwords do not match")
        return is_valid

    @staticmethod
    def login(data):
        this_user = User.getEmail(data['email'])
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['user_id'] = this_user.id
                session['user_name'] = f'{this_user.firstName} {this_user.lastName}'
                return True
        flash("Your login email or password was wrong.")
        return False

#  Saves data to db
    @classmethod
    def create_user(cls, data):
        if not cls.validate_user(data):
            return False
        user_info = cls.register(data)
        query = """
        INSERT INTO users (firstName, lastName, email, password)
        VALUES (%(firstName)s, %(lastName)s, %(email)s, %(password)s)
        ;"""
        user_id = connectToMySQL(cls.db).query_db(query, user_info)
        session['user_id'] = user_id
        session['user_name'] = f'{user_info["firstName"]} {user_info["lastName"]}'
        return user_id
    
    @staticmethod
    def register(data):
        run_data = {
            'email': data['email'],
            'firstName': data['firstName'],
            'lastName': data['lastName'],
            'password': bcrypt.generate_password_hash(data['password'])
        }
        print('!?!?!?!?!?!?', run_data)
        return(run_data)
    
    @classmethod
    def getAll(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users
    
    @classmethod
    def getOne(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def getEmail(cls, email):
        data = {'email': email}
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def save(cls, data):
        query ="""INSERT INTO users 
        (firstName, lastName, email, password) VALUES
        (%(firstName)s, %(lastName)s, %(email)s, %(password)s);"""
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = """UPDATE users 
        SET
        firstName = %(firstName)s,
        lastName = %(lastName)s,
        email = %(email)s,
        password = %(password)s"""

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM users WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)