from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    college = Column(String)


class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    college = Column(String)


class BookModel(Base):
    __tablename__ = 'collageBooks'
    id = Column(Integer, primary_key=True, index=True)
    bookName = Column(String)
    bookAuthor = Column(String)
    count = Column(Integer)
    shelfNumber = Column(Integer)
    racNumber = Column(Integer)
    position = Column(Integer)


class QuestionPaperModel(Base):
    __tablename__ = 'collageQuestionPapers'
    id = Column(Integer, primary_key=True, index=True)
    qnSubName = Column(String)
    qnMonth = Column(String)
    qnScheme = Column(Integer)
    qnSemester = Column(Integer)
    qnYear = Column(Integer)
    qnLink = Column(String)

