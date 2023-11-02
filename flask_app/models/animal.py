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
        self.user = []

        @staticmethod
        def validate(animal):
            isValid = True
            if len(animal['nickName']) < 2:
                isValid = False
                flash('Please use at least 2 characters for the nickname')
            if len(animal['species']) < 2:
                isValid = False
                flash('Please use at least 2 characters for the species')
            if len(animal['locationFound']) < 7:
                isValid = False
                flash('Please use at least 7 characters for the location')
            if len(animal['injury']) < 10:
                isValid = False
                flash('Please use at least 10 characters to describe the injury')
            return isValid

    @classmethod
    def getAll(cls):
        query = 'SELECT * FROM animals;'
        results = connectToMySQL(cls.db).query_db(query)
        animals = []
        for row in results:
            animals.append(cls(row))
        return animals
    
    @classmethod
    def getOne(cls, data):
        query = "SELECT * FROM animals WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def save(cls, data):
        query = """INSERT INTO animals
        (nickName, species, locationFound, injury) VALUES
        (%(nickName)s, %(species)s, %(locationFound)s, %(injury)s);"""
        return connectToMySQL(cls.db).query_db(query, data)
    
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