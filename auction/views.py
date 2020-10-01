from flask import Blueprint, render_template, request, session
from flask_login import current_user
from .models import Item
bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    #items = Item.query.all()
    return render_template('index.html') #,items=items)
    #TODO: implement the db so that this can be fixed

#TODO: search route like in the workshop project

@bp.route('/wishlist') #Possibly move this to another file?
def wishlist():
    #get the wishlist items of the current user
    return render_template('wishlist.html') #,include the items
    #TODO: implement the db so that this can be fixed
