from msilib.schema import Class
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.session import User
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Area:
    data_name = "medcenter"
    def __init__(self, data):
        self.id = data['id']
        self.area_name = data['area_name']

    @classmethod
    def load_area(cls):  
        query = "SELECT * FROM areas;"
        results = connectToMySQL(cls.data_name).query_db(query)
        all_areas = []
        for area in results:
            all_areas.append(cls(area))
        return all_areas
    
    ##Contador de total de areas en centro medico
    @classmethod
    def count_areas(cls):
        query = "SELECT COUNT(areas.id) AS total FROM areas;"
        result = connectToMySQL(cls.data_name).query_db(query)
        print(result)
        return result

class Note:
    data_name = "medcenter"
    def __init__(self,data):
        self.id = data['id']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def add_note(cls, data):
        query = "INSERT INTO notes(description, created_at, updated_at) VALUES (%(description)s, NOW(), NOW());"
        new_note = connectToMySQL(cls.data_name).query_db(query, data)
        return new_note


    @classmethod
    def update_note(cls, data):
        query = "UPDATE notes SET description=%(description)s, updated_at = NOW() WHERE notes.id=%(id)s;"
        return connectToMySQL(cls.data_name).query_db(query,data)

    @staticmethod
    def validate_note(note):
        is_valid = True
        if len(note["description"]) < 20:
            flash("Debes registrar lo sucedido en la sesión", "notes")
            is_valid = False
        return is_valid
    