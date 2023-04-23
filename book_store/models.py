from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime


#Adding flask security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

#import secerets model (from python) generates a taken for each user
import secrets


#import flask login to check for an authentation user and store current user
from flask_login import UserMixin, LoginManager
#import flask marshmellow to help create our schemas
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    firstname = db.Column(db.String(150), nullable = True, default = '')
    lastname = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String(150), nullable = True, default = '')
    username = db.Column(db.String(150), nullable = False)
    date_of_birth = db.Column(db.DateTime, nullable = True)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    book = db.relationship('Book', backref = 'owner', lazy = True)

    def __init__(self, email, username, firstname = '', lastname = '', password='', date_of_birth = ''):

        self.id = self.set_id()
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = self.set_password(password)
        self.username = username
        self.date_of_birth = date_of_birth
        self.token = self.set_token(24)

    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_id(self):
        return str(uuid.uuid4())

    def __repr__(self):
        return f"User {self.email} has been added to the database..!"
    


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    published_date = db.Column(db.Date, nullable=False, default=datetime.now().date())
    publisher = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(13), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(300), nullable=True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)


    def __init__(self, title, author, published_date, publisher, isbn, description, price, stock_quantity, user_token, image_url=None, id = ''):
        self.title = title
        self.author = author
        self.published_date = published_date
        self.publisher = publisher
        self.isbn = isbn
        self.description = description
        self.price = price
        self.stock_quantity = stock_quantity
        self.image_url = image_url
        self.user_token = user_token

    def __repr__(self):
        return f"Book('{self.title}', '{self.author}')"
    
    def set_id(self):
        return str(uuid.uuid4())
    


class BookSchema(ma.Schema):
    class Meta:
        fields = ['id', 'title', 'author', 'published_date', 'publisher', 'isbn', 'description', 'price', 'stock_quantity', 'image_url']

book_schema = BookSchema()
books_schema = BookSchema(many=True)