import sqlalchemy as db
from flask import Flask, jsonify, request
from flask_cors import CORS
from db.database import Database
from api.question import ExecuteQuestion
from api.answer import ExecuteAnswer
from api.menu import ExecuteMenu

class Server(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CORS(self)
        self.config.from_object(f"config")

        # Database
        Database.setConfig(self.config['DATABASE_URI'])

        # Routers
        execute_menu = ExecuteMenu()
        self.route("/api/menu")(execute_menu.load_menu)

        execute_question = ExecuteQuestion()
        self.route("/api/question")(execute_question.load_question)
        self.route("/api/question", methods=['POST'])(execute_question.add_question)
        self.route("/api/question/<question_id>", methods=['DELETE'])(execute_question.delete_question)

        execute_answer = ExecuteAnswer()
        self.route("/api/answer", methods=['POST'])(execute_answer.add_answer)

app = Server("server")
print("Server is running")