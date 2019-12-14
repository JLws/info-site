import sqlalchemy as db

class Database(object):
    CONFIG = {}

    @staticmethod
    def setConfig(database):
        engine = db.create_engine(database)
        Database.CONFIG['engine'] = engine
        Database.CONFIG['connect'] = engine.connect()