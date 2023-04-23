from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Email

class UserLoginForms(FlaskForm):


    firstname = StringField('First Name', validators = [DataRequired()])
    lastname = StringField('Last Name', validators = [DataRequired()])
    username = StringField('Username', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    date_of_birth = DateField('Date of Birth (YYYY-MM-DD)', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()]) #, EqualTo('confirm_password', message='Passwords must match')])
    #confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit_button = SubmitField()



class BookForm(FlaskForm):
    title = StringField('Title')
    author = StringField('Author')
    published_date = StringField('Published Date (YYYY-MM-DD)')
    publisher = StringField('Publisher')
    isbn = StringField('ISBN')
    description = StringField('Description')
    price = DecimalField('Price', places=2)
    stock_quantity = IntegerField('Stock Quantity')
    image_url = StringField('Image URL')
    submit_button = SubmitField()