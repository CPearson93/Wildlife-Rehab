from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user

class Animal:
    db = 'wildlife_schema'
    def __init__(self, data):
        self.id = data['id']
        self.nickName = data['nickName']
        self.species = data['species']
        self.locationFound = data['locationFound']
        self.injury = data['injury']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.user = None

    @staticmethod
    def validate_animal(animal):
        is_valid = True
        if len(animal['nickName']) < 2:
            is_valid = False
            flash('Please use at least 2 characters for the nickname')
        if len(animal['species']) < 2:
            is_valid = False
            flash('Please use at least 2 characters for the species')
        if len(animal['locationFound']) < 3:
            is_valid = False
            flash('Please use at least 3 characters for the location')
        if len(animal['injury']) < 5:
            is_valid = False
            flash('Please use at least 5 characters to describe the injury')
        return is_valid

    @classmethod
    def getAll(cls):
        query = 'SELECT * FROM animals;'
        results = connectToMySQL(cls.db).query_db(query)
        animals = []
        for row in results:
            animals.append(cls(row))
        return animals
    
    @classmethod
    def getOne(cls, id):
        data = {'id': id}
        query = "SELECT * FROM animals WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        print (results)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def save(cls, data):
        if not cls.validate_animal(data):
            return False
        animal_info = cls.register(data)
        query = """
        INSERT INTO animals (user_id, nickName, species, locationFound, injury)
        VALUES (%(user_id)s, %(nickName)s, %(species)s, %(locationFound)s, %(injury)s)
        ;"""
        animal_id = connectToMySQL(cls.db).query_db(query, animal_info)
        return animal_id
    
    @staticmethod
    def register(data):
        run_data = {
            "user_id": session['user_id'],
            'nickName': data['nickName'],
            'species': data['species'],
            'locationFound': data['locationFound'],
            'injury': data['injury']
        }
        print('!?!?!?!?!?!?', run_data)
        return(run_data)
    
    @classmethod
    def update(cls, data):
        query = """UPDATE animals SET
        nickName = %(nickName)s,
        species = %(species)s,
        locationFound = %(locationFound)s,
        injury = %(injury)s,"""

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM animals WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def animalUser(cls, data):
        query = """SELECT * FROM animals
        LEFT JOIN users ON animals.user_id = users.id where animals.id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        for row in results:
            animals = cls(row)
            userData = {
                'id': row ['user.id'],
                'firstName': row['firstName'],
                'lastName': row['lastName'],
                'email': row['email'],
                'password': row['password'],
                'createdAt': row['user.createdAt'],
                'updatedAt': row['user.updatedAt'],
            }
            animals.user = user.User(userData)
        return animals