from flask import Blueprint,render_template,request,flash,redirect
from website.models import Users
from werkzeug.security import check_password_hash,generate_password_hash
from website import db
from flask_login import login_user,logout_user,current_user,login_required

auth = Blueprint('auth',__name__)

@auth.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['Password']
        user = Users.query.filter_by(email = email).first()
        if user:
            if password:
                if check_password_hash(user.password,password):
                    login_user(user = user,remember = True)
                    flash('Logged In',category = 'success')
                else:
                    flash('Incorrect Details',category = "error")
            else:
                flash("Enter Password",category = 'error')
        else:
            flash('Invalid Email',category = 'error')
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return "logout page"

@auth.route('/signup',methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form['Name']
        email = request.form['Email']
        password = request.form['Password']
        cpassword = request.form['Password1']
        if len(name) < 3:
            flash('Name Is Too Short',category = "error")
        elif len(email) < 4:
            flash('Email Is Too Short',category = "error")
        elif password != cpassword:
            flash('Passwords Do Not Match',category = "error")
        else:
            new_user = Users(name = name, email = email , password = generate_password_hash(password,method = "sha256"))
            db.session.add(new_user)
            db.session.commit()
            flash('Account Created',category = "success")
            return redirect('/login')
    return render_template('signup.html')