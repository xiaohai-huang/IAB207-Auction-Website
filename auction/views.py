from flask import Blueprint, render_template, request, session
from flask_login import current_user,login_required
from .models import Item, Bid, Watchlist, BookCategory, Wish, Image
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
    image_thumbnails = db.session.query(Image).join(Item, Item.id == Image.item_id, isouter=True).group_by(Item.id).all()
    return render_template('index.html', items = items_info, show_category_links = True, scifi_count = scifi_count,
    fantasy_count = fantasy_count, mystery_count=mystery_count, autobio_count=autobio_count,
    autograph_count=autograph_count, nonfic_count=nonfic_count, image_thumbnails=image_thumbnails)

@bp.route('/search/<category>')
def search(category):
    # check that the category enum value exists
    if BookCategory[category]:
        # use filter to search for matching items
        items_info = db.session.query(Item,func.count(Bid.id),func.max(Bid.bid_price)).\
        outerjoin(Bid,Item.id==Bid.item_id).\
        order_by(Item.item_datetime.desc()).\
        group_by(Item.id).filter(Item.book_category==category).all()
        image_thumbnails = db.session.query(Image).join(Item, Item.id == Image.item_id, isouter=True).group_by(Item.id).all()
        # render index.html with items
        return render_template('index.html', items=items_info, show_category_links = False, book_category = category, image_thumbnails=image_thumbnails)


@bp.route('/watchlist') #Possibly move this to another file?
@login_required
def watchlist():
    #get the wishlist items of the current user
    watchlist = Watchlist.query.filter(Watchlist.user_id == current_user.id).first()
    if watchlist != None:
        items_info = db.session.query(Wish, Item, func.count(Bid.id),func.max(Bid.bid_price)).\
            outerjoin(Wish, Item.id == Wish.item_id).\
            outerjoin(Bid,Item.id==Bid.item_id).\
            filter_by(Wish.watchlist_id == watchlist.id).\
            order_by(Item.item_datetime.desc()).\
            group_by(Item.id).all()
        return render_template('wishlist.html', items = items_info)
    else:
        return render_template('wishlist.html')
