from flask import Blueprint, render_template, request, session
from flask_login import current_user
from .models import Item
bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    #items = Item.query.all()
    return render_template('index.html') #,items=items)
    #Must implement the db so that this can be fixed