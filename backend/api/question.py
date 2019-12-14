from helper.request import Request as RequestClass
from db.database import Database
import sqlalchemy as db
from flask import jsonify, request

class ExecuteQuestion(RequestClass):

    def add_question(self): # POST
        fields = {'name': '', 'email': '', 'question': ''}
        error = {}
        try:
            self.Parameters(fields, request.form, error) # parse parameters
            question_table = db.Table('questions', db.MetaData(), autoload=True, autoload_with=Database.CONFIG['engine'])
            query = db.insert(question_table, values=fields)
            Database.CONFIG['connect'].execute(query)

        except Exception as e:
            return jsonify({ 'result': False, 'error': str(e) })

        return jsonify({ 'result': True })

    def load_question(self): # GET
        query = ''
        question_table = db.Table('questions', db.MetaData(), autoload=True, autoload_with=Database.CONFIG['engine'])
        try: # load one question
            query = db.select([question_table]).where(question_table.c.id == int(request.args.get('qid')))
            result = Database.CONFIG['connect'].execute(query)
            return_data = {}
            for item in result.fetchall(): # for one question
                return_data = {
                    'name': item.name,
                    'email': item.email,
                    'text': item.question,
                    'date': item.date
                }

            return jsonify({ 'payload': return_data })

        except: # load questions
            offset = request.args.get('offset') if request.args.get('offset') != None else 0
            limit = request.args.get('limit') if request.args.get('limit') != None else 10
            query = db.select([question_table]).offset(offset).limit(limit)
            result = Database.CONFIG['connect'].execute(query)
            return_data = []
            for item in result.fetchall(): # for all question
                return_data.append({
                    'name': item.name,
                    'email': item.email,
                    'text': item.question,
                    'date': item.date
                })

            return jsonify({ 'payload': return_data })

    def remove_question(self, question_id): # DELETE
        try:
            qid = int(question_id)
            question_table = db.Table('questions', db.MetaData(), autoload=True, autoload_with=Database.CONFIG['engine'])
            query = db.delete(question_table).where(question_table.c.id==qid)
            Database.CONFIG['connect'].execute(query)
            return jsonify({ 'result': True })

        except Exception as e:
            return jsonify({ 'result': str(e) })
