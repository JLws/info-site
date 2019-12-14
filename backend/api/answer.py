from helper.request import Request as RequestClass
from db.database import Database
import sqlalchemy as db
from flask import jsonify, request

class ExecuteAnswer(RequestClass):

    def add_answer(self): # POST
        fields = {'question_id': 0, 'name': '', 'answer': ''}
        error = {}
        try:
            self.Parameters(fields, request.form, error) # parse parameters
            answer_table = db.Table('answers', db.MetaData(), autoload=True, autoload_with=Database.CONFIG['engine'])
            query = db.insert(answer_table, fields)
            Database.CONFIG['connect'].execute(query)

        except Exception as e:
            return jsonify({ 'result': False, 'error': str(e) })

        return jsonify({ 'result': True })