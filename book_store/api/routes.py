from flask import Blueprint, request, jsonify
from book_store.helpers import token_required
from book_store.models import db, book_schema, books_schema, Book
from datetime import datetime

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
@token_required
def getdata(our_user):
    return {'some': 'value'}

@api.route('/books', methods=['POST'])
@token_required
def create_book(our_user):
    title = request.json['title']
    author = request.json['author']
    published_date = datetime.strptime(request.json['published_date'], '%Y-%m-%d').date()
    publisher = request.json['publisher']
    isbn = request.json['isbn']
    description = request.json.get('description', None)
    price = request.json['price']
    stock_quantity = request.json['stock_quantity']
    image_url = request.json.get('image_url', None)
    user_token = our_user.token

    print(f"User Token: {our_user.token}")
    
    book = Book(title=title, author=author, published_date=published_date, publisher=publisher,
                isbn=isbn, description=description, price=price, stock_quantity=stock_quantity,
                image_url=image_url, user_token= user_token)

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)

    return jsonify(response)


# Retrieve (READ) all books
@api.route('/books', methods=['GET'])
@token_required
def get_books(our_user):
    owner = our_user.token
    books = Book.query.filter_by(user_token = owner).all()
    response = books_schema.dump(books)

    return jsonify(response)

# Retrieve one book by id
@api.route('/books/<id>', methods=['GET'])
@token_required
def get_book(our_user, id):
    
    if id:
        book = Book.query.get(id)
        response = book_schema.dump(book)
        return jsonify(response)
    else:
        return jsonify({'message': 'Book not found'}), 404


# Update book by id
@api.route('/books/<id>', methods=['PUT'])
@token_required
def update_book(our_user, id):
    book = Book.query.get(id)
    if book:
        book.title = request.json['title']
        book.author = request.json['author']
        book.published_date = request.json['published_date']
        book.publisher = request.json['publisher']
        book.isbn = request.json['isbn']
        book.description = request.json['description']
        book.price = request.json['price']
        book.stock_quantity = request.json['stock_quantity']
        book.image_url = request.json['image_url']
        book.user_token = our_user.token

        db.session.commit()
        response = book_schema.dump(book)
        return jsonify(response)
    else:
        return jsonify({'message': 'Book not found'}), 404


# Delete book by id
@api.route('/books/<id>', methods=['DELETE'])
@token_required
def delete_book(our_user, id):
    book = Book.query.get(id)
    if book:
        db.session.delete(book)
        db.session.commit()
        response = book_schema.dump(book)
        return jsonify(response)
    else:
        return jsonify({'message': 'Book not found'}), 404