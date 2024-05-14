from database.database import engine, Base, session_factory
from database.models import Book, User



class ORM:
    @staticmethod
    def create_tables():
        Base.metadata.create_all(engine)

    @staticmethod
    def drop_tables():
        Base.metadata.drop_all(engine)

    @staticmethod
    def add_user(user):
        with session_factory() as sesion:
            user_new = sesion.query(User).filter(User.username == user.username).first()
            if not user_new:
                sesion.add(user)
                sesion.commit()
            return "Користувач уже є"
    @staticmethod
    def auth_username(username):
        with session_factory() as sesion:
            username_new = sesion.query(User).filter(User.username == username).first()
            
            if username_new:
                return True
            return False
    def auth_password(password):
        with session_factory() as sesion:
            password_new = sesion.query(User).filter(User.password == password).first()
            if password_new:
                return True
            return False

    @staticmethod
    def add_book(book):
        with session_factory() as sesion:
            sesion.add(book)
            sesion.commit()
    @staticmethod
    def get_all_books():
        with session_factory() as sesion:
            books = sesion.query(Book).all()
            return books
    @staticmethod
    def get_book_by_author(author):
        with session_factory() as sesion:
            books = sesion.query(Book).filter(Book.author == author).all()
            return books
    @staticmethod
    def delete_author(book_name):
        with session_factory() as sesion:
            book = sesion.query(Book).filter(Book.name == book_name).first()
            if book:
                sesion.delete(book)
                sesion.commit()
                return True
            else:
                return False
    @staticmethod
    def refil_book(name,new_book):
        with session_factory() as sesion:
            book = sesion.query(Book).filter(Book.name == name).first()
            if book:
                book.name = new_book.name
                book.author = new_book.author
                book.pages = new_book.pages 
                sesion.commit() 
                return book
            else:
                return None
    # @staticmethod
    # def add_record(record):
    #     with session_factory() as session:
    #         session.add(record)
    #         session.commit()

    # @staticmethod
    # def get_all_users():
    #     with session_factory() as session:
    #         users = session.query(User).all()
    #         return users
