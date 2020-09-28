from flask import Blueprint
from flask_login import current_user
bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    if current_user.is_authenticated!=False:

        return f'<h1>{current_user.username}<h1>'
    else:
        return 'welcome, nobody'