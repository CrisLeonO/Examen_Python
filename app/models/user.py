from app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime

import re
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    db_name = 'user_db'

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.alias = data['alias']
        self.email = data['email']
        self.password = data['password']
        self.birthday = data['birthday']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #  Create one User
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (name , alias, email, password, birthday, created_at, updated_at) VALUES ( %(name)s, %(alias)s, %(email)s, %(password)s, %(birthday)s, CURRENT_TIMESTAMP, NOW());"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        print(result)
        return result

    # Get user by email

    @classmethod
    def get_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if len(result) < 1:
            return False
        user = User(result[0])
        return user

    # Get All Users

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    # Get one user

    @classmethod
    def get__one_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if len(result) < 1:
            return False
        user = User(result[0])
        return user

    @staticmethod
    def validate_user(user):
        is_valid = True

        name_regex = re.compile(r'^[a-zA-Z ]+$')

        if len(user['name']) < 3 or not name_regex.match(user['name']):
            flash('Name is not valid', 'register')
            is_valid = False

        if len(user['alias']) < 3:
            flash('Alias is not valid', 'register')
            is_valid = False

        if not email_regex.match(user['email']):
            flash('Invalid email address.', 'register')
            is_valid = False

        if len(user['password']) < 8:
            flash('Password should be at least 8 characters.', 'register')
            is_valid = False

        if user['password'] != user['conf_password']:
            flash('Passwords do not match.', 'register')
            is_valid = False

        if user['birthday'] == '':
            flash('You need to enter a date of birth', 'register')
            is_valid = False

        if user['birthday'] != '':
            age = datetime.today() - \
                datetime.strptime(user['birthday'], '%Y-%m-%d')
            print(age.total_seconds()/(60*60*24*365.25))

            if age.total_seconds()/(60*60*24*365.25) < 16:
                flash('You should be at least 16 years old to register', 'register')
                is_valid = False

        return is_valid
