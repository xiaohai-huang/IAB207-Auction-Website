from flask import ( 
    Blueprint, flash, render_template, request, url_for, redirect
) 
from werkzeug.security import generate_password_hash,check_password_hash
from auction.forms import LoginForm,RegisterForm
from flask_login import login_user, login_required,logout_user
from auction import db
from auction.models import User


#create a blueprint
bp = Blueprint('auth', __name__,url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login(): #view function
    # print('In Login View function')
    login_form = LoginForm()
    error=None
    if(login_form.validate_on_submit()==True):
        user_name = login_form.user_name.data
        password = login_form.password.data
        u1 = User.query.filter_by(username=user_name).first()
        if u1 is None:
            error='Incorrect user name'
        elif not check_password_hash(u1.password_hash, password): # takes the hash and password
            error='Incorrect password'
        if error is None:
            login_user(u1)
            nextp = request.args.get('next') #this gives the url from where the login page was accessed
            # print(nextp)
            if nextp is None or not nextp.startswith('/'):
                return redirect(url_for('main.index'))
            return redirect(nextp)
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')

@bp.route('/register', methods=['GET','POST'])
def register():
    register = RegisterForm()
    #the validation of form submis is fine
    if (register.validate_on_submit() == True):
            #get username, password and email from the form
            uname =register.user_name.data
            pwd = register.password.data
            email=register.email_id.data
            contact_num = register.contact_number.data
            address = register.address.data
            #check if a user exists
            u1 = User.query.filter_by(username=uname).first()
            if u1:
                flash('User name already exists, please login')
                return redirect(url_for('auth.login'))
            # don't store the password - create password hash
            pwd_hash = generate_password_hash(pwd)
            #create a new user model object
            new_user = User(username=uname, password_hash=pwd_hash, email_address=email,
                            contact_number=contact_num ,address=address)
            db.session.add(new_user)
            db.session.commit()
            #commit to the database and redirect to HTML page
            return redirect(url_for('main.index'))
    #the else is called when there is a get message
    else:
        return render_template('user.html', form=register, heading='Register')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    # redirectr to index page
    return redirect(url_for('main.index'))
