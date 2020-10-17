
from flask_wtf import FlaskForm
from wtforms.fields import (TextAreaField, SubmitField, StringField,
                            PasswordField, SelectField, MultipleFileField)
from wtforms import FloatField, BooleanField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed, DataRequired
# add the types of files allowed as a set
ALLOWED_FILE = {'png', 'jpg', 'JPG', 'PNG'}

# creates the login information


class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[
                            InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[
                             InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form


class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[
                           Email("Please enter a valid email")])

    # add buyer/seller - check if it is a buyer or seller hint : Use RequiredIf field

    user_type = SelectField(u'Role', choices=[('buyer', 'Buyer'), ('seller', 'Seller')],
                            validators=[InputRequired("A role should be selected")])
    contact_number = StringField(
        "Contact Number", validators=[InputRequired()])
    address = StringField("Address", validators=[InputRequired()])
    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                                                     EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    # submit button
    submit = SubmitField("Register")

# TODO: ADD AUCTION


class BidForm(FlaskForm):
    bid_price = FloatField("Bid Price", validators=[
                           InputRequired("A bid price is required!")])
    agree = BooleanField("I agree to place the specified bid",
                         validators=[DataRequired()])
    bid = SubmitField("Place Bid")


class BookCreationForm(FlaskForm):
    book_title = StringField("Book Title", validators=[
                             InputRequired('Book Title is required!')])
    isbn = StringField("ISBN", validators=[InputRequired("ISBN is required!")])
    author = StringField("Author", validators=[
                         InputRequired("Author name is required!")])

    category = SelectField(u'Category', choices=[
        ('SCIENCE_FICTION', 'Science Fiction'), ('FANTASY', 'Fantasy'), ('MYSTERY', 'Mystery'), ('AUTOBIOGRAPHY', 'Autobiography'), ('AUTOGRAPHED', 'Autographed Works'), ('NON_FICTION', 'Non-Fiction')],
        validators=[InputRequired("A specific category should be selected!")])

    book_condition = SelectField(u'Book Condition', choices=[
        ('UNTOUCHED', 'Untouched'), ('VERY_GOOD', 'Very good'), ('GOOD', 'Good - used'), ('WEAR_AND_TEAR', 'Some wear and tear'), ('WORN', 'Worn')],
        validators=[InputRequired("A specific condition should be selected!")])

    autograph_status = SelectField(u'Autograph Status',
                                   choices=[('XX', 'Specify if the book is autographed'),
                                            ('TRUE', 'True'),
                                            ('FALSE', 'False')],
                                   validators=[InputRequired(
                                       "A autograph status should be selected")],
                                   default="XX")
    # no sure why file type validator does not work.
    images = MultipleFileField("Images", validators=[DataRequired("At least one image should be uploaded!"),
                                                     FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])

    listing_title = StringField("Listing Title", validators=[
                                InputRequired("A listing title is required!")])
    description = TextAreaField("Description", validators=[
                                InputRequired("A description is required!")])
    starting_bid = FloatField("Starting Bid", validators=[
                              InputRequired("A starting bid is required!")])
    agree = BooleanField("By submitting this listing, I certify that the information given is accurate to the best of my knowledge.",
                         validators=[DataRequired()])
    submit = SubmitField("Create")
    reset = SubmitField("Reset")
