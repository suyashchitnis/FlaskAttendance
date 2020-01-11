from flask import render_template, url_for, flash, redirect, request,session,Response
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm,StudentStoreForm
from flaskblog.models import User, Post, Stud
from flask_login import login_user, current_user, logout_user, login_required
import datetime,os
from werkzeug import FileStorage
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from io import BytesIO


UPLOAD_FOLDER = os.path.dirname(__file__)

app.config['UPLOAD_FOLDER'] = "flaskblog/images/"

posts = [
    {
        'Course': 'MS-CIT',
        'Batch': 'May',
        'NoOfStudent':30,
        'Trainer':'U. K. Chitnis'
    },
    {
        'Course': 'Tally',
        'Batch': 'June',
        'NoOfStudent':10,
        'Trainer':'U. K. Chitnis'
    }
]

@app.after_request
def after_request(response):
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return response

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if user and bcrypt.check_password_hash(user.password, form.password.data):
        if user and user.password==form.password.data:
            session['user']=form.email.data
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    session['user']=None
    logout_user()
    return redirect(url_for('home'))

def get_last_id():
    all = Stud.query.all()
    return len(all)
    
@app.route("/student",methods=['GET','POST'])
@login_required
def Student():
    form = StudentStoreForm(CombinedMultiDict((request.files, request.form)))
    form.Id.data = get_last_id()+1
    # if request.method == 'POST':
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part','error')
            return redirect(request.url)
        file = form.file.data
        print(file)
        # if user does not select file, browser also
        # submit a empty part without filename
        if file == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            # filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], form.sname.data+".png"))


    if form.validate_on_submit():
        student = Stud(Id=form.Id.data
                    , sname=form.sname.data
                    , sdob=form.sdob.data
                    , saddress=form.saddress.data
                    , slandmark=form.slandmark.data
                    , saddmission=form.saddmission.data
                    , file=bytes(str(form.file.data), encoding='utf-8'))
        
        db.session.add(student)
        db.session.flush()
        db.session.commit()
        flash('The student data is added', 'success')
        return redirect(url_for('home'))
    return render_template("StudentStore.html",form=form)

@app.route("/account")
@login_required
def account():
    if session['user']:
        return render_template('account.html', title='Account')
    flash("The user is not logged in","error")
    return redirect(url_for("logout"))

import sqlite3 as sql
def get_table(table_name):
    conn=sql.Connection('./flaskblog/site.db')
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name}")
    return [dict(i) for i in cur.fetchall()]

@app.route("/remove")
@login_required
def Remove():
    if session['user']:
        table=get_table("Student")
        return render_template('remove.html', title='Remove', table=table)
    flash("The user is not logged in","error")
    return redirect(url_for("logout"))

@app.route('/remove/doRemove')
def doRemove():
    data = request.args.get('data')
    print(data)
    delete = Stud.query.filter_by(ID=data).first()
    print(delete)
    db.session.delete(delete)
    db.session.commit()
    flash("The student with ID:%s is deleted"%(data),"success")
    return redirect(url_for("Remove"))
