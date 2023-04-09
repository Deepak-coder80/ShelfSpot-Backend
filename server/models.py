from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True,nullable=False)
    password = Column(String,nullable=False)
    collage = Column(String, unique=True,nullable=False)
    student = relationship('Student',back_populates="admin")
    books = relationship('BookModel',back_populates='book')
    qn_papers = relationship('QuestionPaperModel',back_populates='qn')

class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True,nullable=False)
    password = Column(String,nullable=False)
    collage = Column(String,ForeignKey('admin.collage'),nullable=False)
    admin = relationship('Admin',back_populates="student")

class BookModel(Base):
    __tablename__ = 'collageBooks'
    id = Column(Integer, primary_key=True, index=True)
    bookName = Column(String,nullable=False)
    bookAuthor = Column(String,nullable=False)
    count = Column(Integer,nullable=False)
    shelfNumber = Column(Integer,nullable=False)
    racNumber = Column(Integer,nullable=False)
    position = Column(Integer,nullable=False)
    collage = Column(String,ForeignKey('admin.collage'),nullable=False)
    book_description = Column(String,nullable=True)
    book_id = Column(Integer, nullable=True)
    book = relationship('Admin', back_populates="books")

class QuestionPaperModel(Base):
    __tablename__ = 'collageQuestionPapers'
    id = Column(Integer, primary_key=True, index=True)
    qnSubName = Column(String,nullable=False)
    qnMonth = Column(String,nullable=False)
    qnScheme = Column(Integer,nullable=False)
    qnSemester = Column(Integer,nullable=False)
    qnYear = Column(Integer,nullable=False)
    qnLink = Column(String,nullable=False)
    collage = Column(String, ForeignKey('admin.collage'), nullable=False)
    qn = relationship('Admin',back_populates="qn_papers")
