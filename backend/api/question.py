from helper.request import Request as RequestClass
from db.database import Database
from db.models.Question import Question, Answer
from flask import jsonify, request

class ExecuteQuestion(RequestClass):

    def add_question(self): # POST
        fields = {'name': '', 'email': '', 'question': ''}
        try:
            self.Parameters(fields, request.form) # parse parameters
            new_question = Question(name=fields['name'], email=fields['email'], question=fields['question'])
            Database.CONFIG['session'].add(new_question)
            Database.CONFIG['session'].commit()

        except Exception as e:
            return jsonify({ 'result': False, 'error': str(e) })

        return jsonify({ 'result': True })

    def load_question(self): # GET
        try: # load one question
            query = Database.CONFIG['session'].query(Question, Answer).outerjoin(Answer, Answer.question_id == Question.id).filter(Question.id == int(request.args.get('qid')))
            result = Database.CONFIG['session'].execute(query)
            return_data = {}
            for item in result.fetchall(): # for one question
                return_data = {
                    'name': item.questions_name,
                    'email': item.questions_email,
                    'text': item.questions_question,
                    'date': item.questions_date,
                }
                if not item.answers_username is None: # load answer
                    return_data['answer'] = {
                        'username': item.answers_username,
                        'answer': item.answers_answer,
                        'date': item.answers_date
                    }

            return jsonify({ 'payload': return_data })

        except: # load questions
            offset = request.args.get('offset') if request.args.get('offset') != None else 0
            limit = request.args.get('limit') if request.args.get('limit') != None else 10
            query = Database.CONFIG['session'].query(Question).offset(offset).limit(limit)
            result = Database.CONFIG['session'].execute(query)
            return_data = []
            for item in result.fetchall(): # for all question
                return_data.append({
                    'name': item.questions_name,
                    'email': item.questions_email,
                    'text': item.questions_question,
                    'date': item.questions_date
                })

            return jsonify({ 'payload': return_data })

    def delete_question(self, question_id): # DELETE
        try:
            question = Database.CONFIG['session'].query(Question).get(int(question_id))
            Database.CONFIG['session'].delete(question)
            Database.CONFIG['session'].commit()
            return jsonify({ 'result': True })

        except Exception as e:
            return jsonify({ 'result': False, 'error': str(e) })
