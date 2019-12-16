from helper.request import Request as RequestClass
from db.database import Database
from db.models.Question import Answer
from flask import jsonify, request

class ExecuteAnswer(RequestClass):

    def add_answer(self): # POST
        fields = {'question_id': 0, 'name': '', 'answer': ''}
        error = {}
        try:
            self.Parameters(fields, request.form, error) # parse parameters
            new_answer = Answer(question_id=fields['question_id'], name=fields['name'], answer=fields['answer'])
            Database.CONFIG['session'].add(new_answer)
            Database.CONFIG['session'].commit()

        except Exception as e:
            return jsonify({ 'result': False, 'error': str(e) })

        return jsonify({ 'result': True })

    def delete_answer(self, answer_id): # DELETE
        try:
            answer = Database.CONFIG['session'].query(Answer).get(int(answer_id))
            Database.CONFIG['session'].delete(answer)
            Database.CONFIG['session'].commit()

        except Exception as e:
            return jsonify({ 'result': False, 'error': str(e) })

        return jsonify({ 'result': True })