from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from book_store.forms import BookForm
from book_store.models import db, Book


site = Blueprint('site',__name__,template_folder='site_templates')



@site.route('/')
def home():
    #print("ooga booga in the terminal")
    return render_template('index.html')

@site.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():

    my_book = BookForm()
    print("Enter main func")

    try:
        print("Enter try")
        if request.method == 'POST' and my_book.validate_on_submit():
            print("Enter if ")
            title = my_book.title.data
            author = my_book.author.data
            published_date = my_book.published_date.data
            publisher = my_book.publisher.data
            isbn = my_book.isbn.data
            description = my_book.description.data
            price = my_book.price.data
            stock_quantity = my_book.stock_quantity.data
            image_url = my_book.image_url.data
            user_token = current_user.token

            book = Book(title=title, author=author, published_date=published_date, publisher=publisher,
                isbn=isbn, description=description, price=price, stock_quantity=stock_quantity,
                image_url=image_url, user_token= user_token)
            print("Book object init")
            
            db.session.add(book)
            db.session.commit()

            return redirect(url_for('site.profile'))

    except:
        raise Exception("Book not created, please check your form and try again!")

    current_user_token = current_user.token

    books = Book.query.filter_by(user_token=current_user_token).all()

    return render_template('profile.html', form=my_book, books=books)
