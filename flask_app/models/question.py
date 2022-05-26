from ..config.mysqlconnection import connectToMySQL
from flask import flash
from ..models import user

class Question:
    db = "mental_health_awareness"

    def __init__(self, data):
        # id
        self.id = data['id']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM questions LEFT JOIN users ON users.id = questions.user_id WHERE questions.id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_by_id_detailed(cls, data):
        query = "SELECT * FROM questions LEFT JOIN users ON users.id = user_id WHERE questions.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data) 
        for row in results:
            new_question = cls(row)
            user_data = { 
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'age': row['age'],
                'username': row['username'],
                'email': row['email'],  
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
            }
            new_question.user = user.User(user_data)
        return new_question

    @classmethod
    def get_questions_by_user_id(cls, data):
        query = "SELECT * FROM questions LEFT JOIN users ON users.id = questions.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        my_questions = []
        for row in results:
            my_questions.append(cls(row))
        return my_questions

    @classmethod
    def create_question(cls, data):
        query = "INSERT INTO questions (comment, user_id) VALUES (%(comment)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update_question(cls, data):
        query = "UPDATE questions SET comment=%(comment)s, user_id=%(user_id)s WHERE questions.id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def destroy_question(cls, data):
        query = "DELETE FROM questions WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    # validate length
    @staticmethod
    def validate_question(data):
        is_valid = True
        if len(data["comment"]) < 10:
            flash("There needs to be at least 10 characters", "question")
            is_valid = False
        return is_valid