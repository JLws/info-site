import sqlalchemy as db
from flask import Flask
from flask_cors import CORS

class Server(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CORS(self)
        self.config.from_object(f"config")

        #Database
        engine = db.create_engine(self.config['DATABASE_URI'])
        self.db = {
            'engine': engine,
            'connect': engine.connect(),
        }

app = Server("server")
print("Server is running")