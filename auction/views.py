from flask import Blueprint, render_template, request, session
from flask_login import current_user
from .models import Item, Bid, Watchlist, BookCategory
from sqlalchemy import func
from auction import db
bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    #bid_counts = Bid.query.all() # is there a better way to do this than querying the entire bid table? :(
    #items = Item.query.order_by(Item.item_datetime.desc()).limit(5).all() # grabs the 5 most recent as per assignment specs
    # item, num bids, highest bid
    items_info = db.session.query(Item,func.count(Bid.id),func.max(Bid.bid_price)).\
        outerjoin(Bid,Item.id==Bid.item_id).\
        order_by(Item.item_datetime.desc()).\
        group_by(Item.id).limit(5).all()

    # not sure if it's possible to get a single count query that will create a '0' entry for a non encountered column
    # it just skips the category otherwise - is there a better way to do this?
    scifi_count = db.session.query(Item.book_category).filter(Item.book_category == BookCategory.SCIENCE_FICTION).count()
    fantasy_count = db.session.query(Item.book_category).filter(Item.book_category == BookCategory.FANTASY).count()
    mystery_count = db.session.query(Item.book_category).filter(Item.book_category == BookCategory.MYSTERY).count()
    autobio_count = db.session.query(Item.book_category).filter(Item.book_category == BookCategory.AUTOBIOGRAPHY).count()
    autograph_count = db.session.query(Item.book_category).filter(Item.book_category == BookCategory.AUTOGRAPHED).count()
    nonfic_count = db.session.query(Item.book_category).filter(Item.book_category == BookCategory.NON_FICTION).count()

    return render_template('index.html', items = items_info, show_category_links = True, scifi_count = scifi_count, 
    fantasy_count = fantasy_count, mystery_count=mystery_count, autobio_count=autobio_count,
    autograph_count=autograph_count, nonfic_count=nonfic_count)

@bp.route('/search/<category>')
def search(category):
    # check that the category enum value exists
    if BookCategory[category]:
        # use filter and like function to search for matching destinations
        items_info = db.session.query(Item,func.count(Bid.id),func.max(Bid.bid_price)).\
        outerjoin(Bid,Item.id==Bid.item_id).\
        order_by(Item.item_datetime.desc()).\
        group_by(Item.id).filter(Item.book_category==category).all()
        # render index.html with few destinations
        return render_template('index.html', items=items_info, show_category_links = False, book_category = category)


@bp.route('/wishlist') #Possibly move this to another file?
def wishlist():
    #get the wishlist items of the current user
    #wishlists = Wishlist.query.filter_by(expression).all()
    #TODO: FIX THE ABOVE STATEMENT
    return render_template('wishlist.html') #,include the items
