from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Database(object):
    CONFIG = {}

    @staticmethod
    def setConfig(database):
        engine = create_engine(database)
        Database.CONFIG['engine'] = engine
        Database.CONFIG['session'] = sessionmaker(bind=engine)()