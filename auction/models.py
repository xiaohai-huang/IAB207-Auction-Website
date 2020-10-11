# need for datetime.now()
from datetime import datetime
from flask_login import UserMixin
from . import db
import enum

class BookCategory(enum.Enum):
    SCIENCE_FICTION = "Science Fiction"
    FANTASY = "Fantasy"
    MYSTERY = "Mystery"
    AUTOBIOGRAPHY = "Autobiography"
    AUTOGRAPHED = "Autographed Works"
    NON_FICTION = "Non Fiction"

class AutographStatus(enum.Enum):
    TRUE = "✔️"
    FALSE = "❌"

class BookCondition(enum.Enum):
    UNTOUCHED = "Untouched"
    VERY_GOOD = "Very good - natural deterioration"
    GOOD = "Good - used"
    WEAR_AND_TEAR = "Some obvious wear and tear"
    WORN = "Visibly worn - heavy deterioration"

class Item(db.Model):
    __tablename__='items'
    id = db.Column(db.Integer, primary_key=True)
    listing_title = db.Column(db.String(64), unique=True, index=True, nullable=False)
    book_title = db.Column(db.String(64), index=True, nullable=False)
    book_category = db.Column(db.Enum(BookCategory), index=True, nullable=False)
    autograph_status = db.Column(db.Enum(AutographStatus), index=True, nullable=False)
    book_condition = db.Column(db.Enum(BookCondition), index=True, nullable=False)
    author_name = db.Column(db.String(64), index=True, nullable=False)
    book_ISBN = db.Column(db.String(64), index=True)
    listing_description = db.Column(db.String(500), nullable=False)
    starting_bid = db.Column(db.Float(2), default=0.01)
    item_status = db.Column(db.String(6), default='Open')
    item_datetime = db.Column(db.DateTime, default=datetime.now())
    #image = db.Column(db.String(60), nullable=False, default='default.jpg')

    # one to many relationship - user can have multiple items
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    #backref
    bids = db.relationship('Bid', backref='item')
    wishes = db.relationship('Wish', backref='item')
    images = db.relationship('Image', backref='item')

class Image(db.Model):
    __tablename__='images'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(60), nullable=False, default='../static/placeholder.jpg')
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))


class Bid(db.Model):
    __tablename__='bids'
    id = db.Column(db.Integer, primary_key=True)
    bid_price = db.Column(db.Float(2), nullable=False)
    bid_datetime = db.Column(db.DateTime, default=datetime.now())

    # one item can have multiple bids - one to many
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    # bid user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class User(db.Model,UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True, nullable=False)
    user_type = db.Column(db.String(6),nullable=False)
    contact_number = db.Column(db.String(100),nullable=False)
    email_address = db.Column(db.String(100), index=True, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    # backrefs
    items = db.relationship('Item', backref='user')
    bids = db.relationship('Bid', backref='user')
    # one watchlist to one user
    watchlist = db.relationship('Watchlist', backref='user', uselist=False)

class Watchlist(db.Model):
    __tablename__='watchlists'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # change watchlist to wishes, correct me if I am wrong.
    wishes = db.relationship('Wish', backref='watchlist')

class Wish(db.Model):
    __tablename__='wishes'
    id = db.Column(db.Integer, primary_key=True)
    watchlist_id = db.Column(db.Integer, db.ForeignKey('watchlists.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    added_datetime = db.Column(db.DateTime, default=datetime.now())
