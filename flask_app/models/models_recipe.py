from flask_app.controllers import controllers_users
import re
from flask_app.models import models_user
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db = 'recipes_db'


class Recipe:

    def __init__(self, recipe):
        self.id = recipe["id"]
        self.name = recipe["name"]
        self.description = recipe["description"]
        self.instructions = recipe["instructions"]
        self.date_made = recipe["date_made"]
        self.under_30 = recipe["under_30"]
        self.created_at = recipe["created_at"]
        self.updated_at = recipe["updated_at"]
        self.user_id = recipe["user_id"] 
        self.user = None

    @classmethod
    def get_one_by_id(cls, recipe_id):

        query = """SELECT * from recipes JOIN users on recipes.user_id= users.id WHERE recipes.id=%(id)s;"""

        data = {
            "id": recipe_id
        }
        results = connectToMySQL(db).query_db(query, data)
        if results:
            recipe_dict = connectToMySQL(db).query_db(query, data)[0]
            print(recipe_dict)
            recipe_obj = Recipe(recipe_dict)

            user_obj = models_user.User({
                "id": recipe_dict['users.id'],
                "first_name": recipe_dict['first_name'],
                "last_name": recipe_dict['last_name'],
                "email": recipe_dict['email'],
                "password": recipe_dict['password'],
                "created_at": recipe_dict['users.created_at'],
                "updated_at": recipe_dict['users.updated_at']

            })
            recipe_obj.user = user_obj
            return recipe_obj
        else:
            return None

    @classmethod
    def get_all(cls):

        query = """
        SELECT * from recipes JOIN users on recipes.user_id = users.id;
        """
        result = connectToMySQL(db).query_db(query)
        print(result)
        recipes = []
        for recipe_dict in result:
            recipe_obj = Recipe(recipe_dict)
            user_obj = models_user.User({
                "id": recipe_dict['users.id'],
                "first_name": recipe_dict['first_name'],
                "last_name": recipe_dict['last_name'],
                "email": recipe_dict['email'],
                "password": recipe_dict['password'],
                "created_at": recipe_dict['users.created_at'],
                "updated_at": recipe_dict['users.updated_at']
            })

            recipe_obj.user = user_obj

            recipes.append(recipe_obj)
        return recipes

    @classmethod
    def save(cls, recipe_data):

        query = """
        INSERT INTO recipes (name, description, instructions, date_made, under_30, user_id) VALUES (%(name)s,%(description)s,%(instructions)s, %(date_made)s, %(under_30)s, %(user_id)s)
                """
        return connectToMySQL(db).query_db(query, recipe_data)
        return

    @classmethod
    def delete_by_id(cls, recipe_id):
        query = """ DELETE from recipes WHERE id=%(id)s"""
        data = {
            "id": recipe_id
        }
        connectToMySQL(db).query_db(query, data)

        return

    @classmethod
    def update_recipe(cls, recipe_data):

        query = """UPDATE recipes 
        Set name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under_30 = %(under_30)s
        Where id =%(id)s;"""
        connectToMySQL(db).query_db(query, recipe_data)
        return

    @staticmethod
    def is_valid(recipe_dict):

        valid = True
        if len(recipe_dict["name"]) == 0:
            valid = False
            flash("Name is required")

        if len(recipe_dict["description"]) == 0:
            valid = False
            flash("Description is required")
        elif len(recipe_dict["description"]) < 3:
            valid = False
            flash("Description must be at least 3 characters.")

        if len(recipe_dict["instructions"]) == 0:
            valid = False
            flash("Instructions is required")
        elif len(recipe_dict["instructions"]) < 3:
            valid = False
            flash("Instructions must be at least 3 characters.")

        if len(recipe_dict["date_made"]) == 0:
            valid = False
            flash("Date made is required")

        if "under_30" not in recipe_dict:
            valid = False
            flash("Recipe length required. ")

        return valid
