from flask import Blueprint
from flask import request
from flask import session
from flask import redirect, url_for
from flask import render_template
from werkzeug.utils import secure_filename
import os
from .models import Item, Wish, Watchlist, Bid, User
from . import db

bp = Blueprint('item', __name__, url_prefix='/items')

@bp.route('/<id>')
def show(id):
    #item = Item.query.filter_by(id=id).first()
    # basically, using id as the url and querying the database with it i.e. books.com/items/1 would return the page of item with id 1
    # put form here
    # render template goes here
    return render_template("item/show.html")#,item=item, form=form, etc)

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