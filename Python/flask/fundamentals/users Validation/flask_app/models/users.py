from flask_app.config.mysqlconnection import connectToMySQL 
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User: 
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod 
    def get_all(cls):
            query = "SELECT * FROM users;"
            results = connectToMySQL('usersCR').query_db(query)
            users = []
            for u in results: 
                users.append( cls(u))
            return users


    @classmethod 
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email) VALUES (%(first_name)s, %(last_name)s, %(email)s);"
        result = connectToMySQL('usersCR').query_db(query, data)
        return result
    

    @classmethod
    def edit(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('usersCR').query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def show(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('usersCR').query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def update(cls,data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL('usersCR').query_db(query,data)


    @classmethod 
    def destroy(cls,data):
        query = "DELETE from users WHERE id = %(id)s;"
        return connectToMySQL('usersCR').query_db(query,data)\

@staticmethod 
def validate_users(users):
    is_valid = True
    if len(users['name']) < 1:
            flash("Name must be at least 1 character.")
            is_valid = False
    if len(users['bun']) < 3:
            flash("Bun must be at least 3 characters.")
            is_valid = False
    if int(users['calories']) < 200:
            flash("Calories must be 200 or greater.")
            is_valid = False
    if len(users['meat']) < 3:
            flash("Bun must be at least 3 characters.")
            is_valid = False
    return is_valid

@staticmethod
def validate_user( user ):
        is_valid = True
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid

@classmethod
def is_valid_user(cls, user):
        is_valid = True

        if len(user["first_name"]) <= 0:
            is_valid = False
            flash("First name is required.")
        if len(user["last_name"]) <= 0:
            is_valid = False
            flash("Last name is required.")
        if len(user["email"]) <= 0:
            is_valid = False
            flash("Email is required.")

