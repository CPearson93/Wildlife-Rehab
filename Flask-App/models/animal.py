from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user

class Animal:
    def __init__(self, data):
        self.id = data['id']
        self.nickName = data['nickName']
        self.species = data['species']
        self.locationFound = data['locationFound']
        self.injury = data['injury']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']