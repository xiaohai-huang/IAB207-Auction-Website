from flask import Blueprint, render_template, request, session
from flask_login import current_user
from .models import Item, Bid
bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    bid_counts = Bid.query.all() # is there a better way to do this than querying the entire bid table? :(
    items = Item.query.order_by(Item.item_datetime.desc()).limit(5).all() # grabs the 5 most recent as per assignment specs
    return render_template('index.html', items = items, bid_counts = bid_counts)

#TODO: search route like in the workshop project

@bp.route('/wishlist') #Possibly move this to another file?
def wishlist():
    #get the wishlist items of the current user
    return render_template('wishlist.html') #,include the items
    #TODO: implement the db so that this can be fixed
