from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime
Base = declarative_base()

class Page(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    image = Column(String(32))
    username = Column(String(32))
    name = Column(String(64))
    content = Column(Text)
    date = Column(DateTime, system=True)