from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
Base = declarative_base()

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    name = Column(String(36))
    email = Column(String(64))
    question = Column(String(128))
    date = Column(TIMESTAMP)
    answer = relationship('Answer')

class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    username = Column(String(32))
    answer = Column(String(128))
    date = Column(TIMESTAMP)