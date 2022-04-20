from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re

DATABASE = 'recipes_schema'
PRIMARY_TABLE = 'recipes'

## Toggle to run all debug statements to track data flow
## True = On, False = Off
debug = False

class Recipe:
    def __init__(self, data:dict) -> None:
        ## INSTANCE ATTRIBUTES SHOULD BE SAME AS TABLE COLUMNS
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.origin_date = data['origin_date']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # ! READ/RETRIEVE/VALIDATE
    @classmethod
    def get_all(cls) -> list:
        query = f"SELECT * FROM {PRIMARY_TABLE};"
        results = connectToMySQL(DATABASE).query_db(query)
        # Make list to return
        recipes_list = []
        for recipe in results:
            # Add instances of the class to the list
            recipes_list.append( cls(recipe) )
        # return list of instances of the class
        return recipes_list

    ## Provide id in dict, query by id, get back 1 user info
    @classmethod
    def get_one(cls, data:dict) -> object:
        query = f"SELECT * FROM {PRIMARY_TABLE} WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return cls(results[0])

    ## Provide column_name in dict, query by column_name, get back 1 user info or False
    @classmethod
    def get_by_col(cls, data:dict) -> object or bool:
        # Only the first key,value pair combo from dict will be checked
        query = f"SELECT * FROM {PRIMARY_TABLE} WHERE { list(data.keys())[0] } = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        # Return an instance class of User if true, else return False
        return cls(result[0]) if result else False

    # ! CREATE
    @staticmethod
    def save(data:dict) -> int:
        query = f"INSERT INTO {PRIMARY_TABLE} ( name, description, instructions, under_30, origin_date, user_id ) VALUES ( %(name)s, %(description)s, %(instructions)s, %(under_30)s, %(origin_date)s, %(user_id)s );"
        return connectToMySQL(DATABASE).query_db( query, data )

    # ! UPDATE
    @classmethod
    def update(cls,data:dict) -> int:
        query = f"UPDATE {PRIMARY_TABLE} SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, under_30=%(under_30)s, origin_date=%(origin_date)s, user_id=%(user_id)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    # ! DELETE
    @staticmethod
    def del_one(data: dict) -> None:
        query = f"DELETE FROM {PRIMARY_TABLE} WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)