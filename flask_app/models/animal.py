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
        self.creator = None

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
        query = """SELECT * FROM animals
        JOIN users ON users.id = animals.user_id;"""
        results = connectToMySQL(cls.db).query_db(query)
        all_animals = []
        for row in results:
            animal = cls(row)
            userData = {
                'id': row ['users.id'],
                'firstName': row['firstName'],
                'lastName': row['lastName'],
                'email': row['email'],
                'password': row['password'],
                'createdAt': row['createdAt'],
                'updateAt': row['updateAt'],
            }
            animal.creator = user.User(userData)
            all_animals.append(animal)
        return all_animals

    @classmethod
    def getOne(cls, id):
        data = {'id': id}
        query = "SELECT * FROM animals WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        print (results)
        if results:
            return (results[0])
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
    def update(cls, data, id):
        if not cls.validate_animal(data):
            return False
        data = cls.register(data)
        query = """UPDATE animals SET
        nickName = %(nickName)s,
        species = %(species)s,
        locationFound = %(locationFound)s,
        injury = %(injury)s,"""
        animal_id = connectToMySQL(cls.db).query_db(query, data)
        return animal_id

    @classmethod
    def delete(cls, num):
        query = 'DELETE FROM animals WHERE id = %(id)s;'
        data = {'id': num}
        return connectToMySQL(cls.db).query_db(query, data)
    
    @staticmethod
    def validate_action(num):
        this_animal = Animal.getOne(num)
        is_valid = True
        if session['user_id'] != this_animal["user_id"]:
            is_valid = False
        return is_valid