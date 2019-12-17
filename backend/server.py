import sqlalchemy as db
from flask import Flask, jsonify, request
from flask_cors import CORS
from db.database import Database
from api.question import ExecuteQuestion
from api.answer import ExecuteAnswer
from api.menu import ExecuteMenu
from api.page import ExecutePage

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
        self.route("/api/answer/<answer_id>", methods=['DELETE'])(execute_answer.delete_answer)
        self.route("/api/answer/<answer_id>", methods=['POST'])(execute_answer.edit_answer)

        execute_page = ExecutePage()
        self.route("/api/page", methods=['GET'])(execute_page.load_page)
        self.route("/api/page", methods=['POST'])(execute_page.add_page)
        self.route("/api/page/<page_id>", methods=['DELETE'])(execute_page.delete_page)
        self.route("/api/page/<page_id>", methods=['POST'])(execute_page.edit_page)

app = Server("server")
print("Server is running")