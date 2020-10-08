from flask import Blueprint
from flask import request
from flask import session
from flask import redirect, url_for
from flask import render_template
from werkzeug.utils import secure_filename
import os
from .models import Item, Wish, Watchlist, Bid, User, Image
from . import db

bp = Blueprint('item', __name__, url_prefix='/items')

@bp.route('/<id>')
def show(id):
    item = Item.query.filter_by(id=id).first() # grab item query data by id
    images = item.images #Image.query.filter_by(item_id = id).all()
    user = User.query.filter_by(id = item.user_id).first() # this is the user who has listed the item, need to pull their username
    bids = Bid.query.filter_by(item_id = item.id).order_by(Bid.bid_datetime.desc()).limit(10).all() # grabs top ten most recent bids
    formatted_datetime = item.item_datetime.strftime("%m/%d/%Y, %H:%M:%S") # formats into a nice datetime that can be used to show item listing date; this is optional
    bidders = db.session.query(User).join(Bid, User.id == Bid.user_id, isouter=True).join(Item, id == Bid.item_id, isouter=True).filter_by(id = Bid.item_id).order_by(Bid.bid_datetime.desc()).group_by(User.id).limit(10).all()
    return render_template("item/show.html", item = item, images = images, user=user, bids = bids, formatted_datetime = formatted_datetime, bidders = bidders)#,item=item, form=form, etc)

@bp.route('/create', methods=['GET', 'POST'])
#TODO: MAKE THE NECESSARY CHANGES TO UNCOMMENT THE COMMENTED CODE
#@login_required
def create():
    # print('Method type: ', request.method)
    # form = AuctionForm()
    # if(form.validate_on_submit()):
    #     db_file_path = check_upload_file(form)
    #     item = Item(form fields)

    #     db.session.add(item)
    #     db.session.commit()
    #     return redirect(url_for('item.create'))
    return render_template('item/create.html')#, form=form)
