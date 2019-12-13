import sqlalchemy as db
from flask import Flask, jsonify, request
from flask_cors import CORS

class Server(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CORS(self)
        self.config.from_object(f"config")

        # Database
        engine = db.create_engine(self.config['DATABASE_URI'])
        self.db = {
            'engine': engine,
            'connect': engine.connect(),
        }

        # Routers
        self.route("/api/menu")(self.menu)
        self.route("/api/question")(self.load_question)
        self.route("/api/question", methods=['POST'])(self.add_question)
        self.route("/api/question/<question_id>", methods=['DELETE'])(self.remove_question)

    def menu(self):
        menu = db.Table('menu', db.MetaData(), autoload=True, autoload_with=self.db['engine'])
        query = db.select([menu])
        result = self.db['connect'].execute(query)
        menudata = []
        for item in result.fetchall():
            item_id, item_name, item_parent, item_url = item
            if len(menudata) == 0:
                if item_parent == None:
                    menudata.append({'id': item_id, 'name': item_name, 'url': item_url, 'child': [] })

                else:
                    menudata.append({'id': item_parent, 'name': '', 'url': '', 'child': [{'name': item_name, 'url': item_url}] })
                
                continue

            for item_menu in menudata:
                if item_parent == None: # add parebt
                    if item_menu['id'] == item_id:
                        item_menu['name'] = item_name
                        item_menu['url'] = item_url

                else: # add child
                    if item_menu['id'] == item_parent:
                        item_menu['child'].append({'name': item_name, 'url': item_url})
                        break

            else: # not found parent
                if item_parent == None: # add parent
                    menudata.append({'id': item_id, 'name': item_name, 'url': item_url, 'child': [] })

                else: # add child
                    menudata.append({'id': item_parent, 'name': '', 'url': '', 'child': [{'name': item_name, 'url': item_url}] })

        return jsonify({ 'payload': menudata })

    def load_question(self):
        query = ''
        question_table = db.Table('questions', db.MetaData(), autoload=True, autoload_with=self.db['engine'])
        try: # load one question
            query = db.select([question_table]).where(question_table.c.id == int(request.args.get('qid')))
            result = self.db['connect'].execute(query)
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
            result = self.db['connect'].execute(query)
            return_data = []
            for item in result.fetchall(): # for all question
                return_data.append({
                    'name': item.name,
                    'email': item.email,
                    'text': item.question,
                    'date': item.date
                })

            return jsonify({ 'payload': return_data })

    def remove_question(self, question_id):
        try:
            qid = int(question_id)
            question_table = db.Table('questions', db.MetaData(), autoload=True, autoload_with=self.db['engine'])
            query = db.delete(question_table).where(question_table.c.id==qid)
            self.db['connect'].execute(query)
            return jsonify({ 'result': True })

        except Exception as e:
            return jsonify({ 'result': str(e) })

    def add_question(self):
        fields = {'name': '', 'email': '', 'question': ''}

        for field in fields: # find fields
            data = request.form.get(field, None)
            if data: # not found
                fields[field] = data

            else: # found
                return jsonify({ 'result': False, 'error': 'Not found ' + field })

        question_table = db.Table('questions', db.MetaData(), autoload=True, autoload_with=self.db['engine'])
        query = db.insert(question_table, values=fields)
        self.db['connect'].execute(query)
        return jsonify({ 'result': True })

app = Server("server")
print("Server is running")