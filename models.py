from sqlalchemy import (create_engine, Column, Integer, String, Date)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///books.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column('Title', String)
    author = Column('Author', String)
    publish_date = Column('Published_Date', Date)
    price = Column('Price', Integer)

    def __repr__(self):
        # return f'<Book(title={self.title}, author={self.author}, publish_date={self.publish_date}, price={self.price})>'
        return f'Title: {self.title} Author: {self.author} Published_Date: {self.publish_date} Price: {self.price}'

# create database
# books.db
# create a model
# title, author, date_published, price
