from sqlalchemy import Column, Integer, String

from database.database import Base


# class User(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     login = Column(String)
#     password = Column(String)
    
#     def __str__(self):
#         return f"{self.id=} {self.name=} {self.login=} {self.password=}"
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    author = Column(String)
    pages = Column(String)
    def __str__(self):
        return f"{self.id=} {self.name=} {self.author=} {self.pages=}"
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    def __str__(self):
        return f"{self.id=} {self.name=} {self.author=} {self.pages=}"


