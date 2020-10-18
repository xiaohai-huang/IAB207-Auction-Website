from flask import Blueprint
from flask import request
from flask import session
from flask import redirect, url_for
from flask import render_template, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
from .models import Item, Wish, Watchlist, Bid, User, Image, BookCategory, BookCondition, AutographStatus
from . import db
from auction.forms import BookCreationForm, BidForm
from sqlalchemy import func, desc
from datetime import datetime
bp = Blueprint('item', __name__, url_prefix='/items')


@bp.route('/<id>')
def show(id):
    item = Item.query.filter_by(id=id).first()  # grab item query data by id
    images = Image.query.filter_by(item_id=id).all()
    # this is the user who has listed the item, need to pull their username
    user = User.query.filter_by(id=item.user_id).first()
    bids = Bid.query.filter_by(item_id=item.id).order_by(
        Bid.bid_datetime.desc()).limit(10).all()  # grabs top ten most recent bids
    # formats into a nice datetime that can be used to show item listing date; this is optional
    formatted_datetime = item.item_datetime.strftime("%m/%d/%Y, %H:%M:%S")
    bidders = db.session.query(User).join(Bid, User.id == Bid.user_id, isouter=True).join(
        Item, id == Bid.item_id, isouter=True).filter_by(id=Bid.item_id).order_by(Bid.bid_datetime.desc()).group_by(User.id).limit(10).all()

    bid_form = BidForm()
    return render_template("item/show.html", item=item, images=images,
                           user=user, bids=bids, formatted_datetime=formatted_datetime,
                           bidders=bidders, bid_form=bid_form)


@bp.route('/<item_id>/bid', methods=["GET", "POST"])
@login_required
def bid(item_id):
    form = BidForm()
    book = Item.query.filter(Item.id == item_id).first()

    if form.validate_on_submit():
        # make sure seller cannot bid on his own book
        if current_user.id == book.user_id:
            flash("You cannot bid on your own book!")
            return redirect(url_for('item.show', id=item_id))

        # get the highest bid
        bids = book.bids
        if len(bids) != 0:
            max_bid_price = bids[0].bid_price
        else:
            max_bid_price = book.starting_bid

        for b in bids:
            if b.bid_price > max_bid_price:
                max_bid_price = b.bid_price
        if form.bid_price.data > max_bid_price:

            bid = Bid(bid_price=form.bid_price.data, item_id=item_id,
                      user_id=current_user.id, bid_datetime=datetime.now())
            db.session.add(bid)
            db.session.commit()
        else:  # erro message less than current bid price
            flash(f"Please eneter a bid that is greater than ${max_bid_price}")
    else:
        if form.bid_price.errors[0] == "Not a valid float value":
            flash("Please enter a valid bid price!")

    return redirect(url_for('item.show', id=item_id))


# add the types of files allowed as a set
ALLOWED_FILE = {'png', 'jpg', 'JPG', 'PNG'}


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    # only seller can create listings
    if(current_user.user_type != "seller"):
        flash("You cannot create a listing as a buyer!")
        return redirect(url_for('main.index'))

    print('Method type: ', request.method)
    form = BookCreationForm()
    if(form.validate_on_submit()):
        listing_title = form.listing_title.data
        book_title = form.book_title.data
        book_category = BookCategory[form.category.data]
        autograph_status = AutographStatus[form.autograph_status.data]
        book_condition = BookCondition[form.book_condition.data]
        author_name = form.author.data
        book_ISBN = form.isbn.data
        listing_description = form.description.data
        starting_bid = form.starting_bid.data
        creator_id = current_user.id

        valid = True
        # ensure the listing_title is unique
        if not Item.query.filter(Item.listing_title == listing_title).first() == None:
            flash("The listing title already exists!", "listing_title_repeated")
            # ensure uploaded files are all images
            valid = False   

        # check file types
        images = request.files.getlist(form.images.name)
        for image in images:
            filename = image.filename
            if not filename.split('.')[1] in ALLOWED_FILE:
                flash('Only supports png, jpg, JPG, PNG', "file_type")
                valid=False
                break
        if valid==False:
            return render_template('item/create.html', form=form)

        new_book = Item(listing_title=listing_title,
                        book_title=book_title,
                        book_category=book_category,
                        autograph_status=autograph_status,
                        book_condition=book_condition,
                        author_name=author_name,
                        book_ISBN=book_ISBN,
                        listing_description=listing_description,
                        starting_bid=starting_bid,
                        user_id=creator_id)
        db.session.add(new_book)
        db.session.commit()
        # link images to the new book
        BASE_PATH = os.path.dirname(__file__)
        for image in images:
            filename = image.filename
            upload_path = os.path.join(
                BASE_PATH + '/static/images', secure_filename(filename))

            db_upload_path = '/static/images/' + secure_filename(filename)
            image.save(upload_path)

            img_model = Image(image=db_upload_path, item_id=new_book.id)
            db.session.add(img_model)
            db.session.commit()

        return redirect(url_for('item.show', id=new_book.id))
    return render_template('item/create.html', form=form)
