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
        self.route("/api/questions")(self.questions)

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

    def questions(self):
        offset = request.args.get('offset') if request.args.get('offset') != None else 0
        limit = request.args.get('limit') if request.args.get('limit') != None else 10
        question = db.Table('questions', db.MetaData(), autoload=True, autoload_with=self.db['engine'])
        query = db.select([question]).offset(offset).limit(limit)
        result = self.db['connect'].execute(query)
        questions = []
        for question in result.fetchall():
            questions.append({
                'name': question.name,
                'email': question.email,
                'text': question.question,
                'date': question.date
            })

        return jsonify({ 'payload': questions })

app = Server("server")
print("Server is running")