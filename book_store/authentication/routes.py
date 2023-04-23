from flask import Blueprint, render_template, request, redirect, url_for, flash
from book_store.forms import UserLoginForms
from book_store.models import User, db
from book_store.models import User, db, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required


auth = Blueprint('auth', __name__, template_folder='auth_templates')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserLoginForms()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            firstname = form.firstname.data
            lastname = form.lastname.data
            email = form.email.data
            password = form.password.data
            username = form.username.data
            date_of_birth = form.date_of_birth.data
            print(email, username)

            user = User(firstname=firstname, lastname=lastname, email=email,
                        password=password, username=username, date_of_birth=date_of_birth)
            db.session.add(user)
            db.session.commit()

            flash(
                f'You have successfully created a user account {username}', 'user-created')

            return redirect(url_for('auth.signin'))

    except:
        raise Exception("Invalid form data. Please check your form")

    return render_template('signup.html', form=form)


@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    print("Enter sign in")
    form = UserLoginForms()
    try:
        print("Enter try")

        if request.method == 'POST':
            print("Enter if")
            email = form.email.data
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()
            print(logged_user)
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                print(login_user)
                flash('You were successfully logged in: Via Email/Password', 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash('Your Email/Password is incorrect', 'auth-failed')
                return redirect(url_for('auth.signin'))
    except:
        print("Enter exception")
        raise Exception('Invalid Form Data: Please Check Your Form')
    return render_template('signin.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))
