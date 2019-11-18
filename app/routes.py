from app import app, models, db
from flask import Flask, render_template, flash, redirect, request
from app.forms import LoginForm, SignInForm
from werkzeug.urls import url_parse
from flask_login import login_user

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form_log_in = LoginForm()
    if form_log_in.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form_log_in.username.data, form_log_in.remember_me.data))
        user = models.User.query.filter_by(Username=form_log_in.username.data).first()
        if user is None or not user.check_password(form_log_in.password.data):
            flash('invalid username or password')
            return redirect('/login/')
        login_user(user, remember=form_log_in.remember_me.data)
        return redirect('/')
    return render_template('login.html', title='Log In', form=form_log_in)

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    form_sign_up = SignInForm()
    if form_sign_up.validate_on_submit() and form_sign_up.password.data == form_sign_up.password2.data:
        #before creating a location query database and see if it exists already
        #if it doesn't, make a location object and add to DB before building user

        #CURRENTLY THIS IS DOING NO VALIDATION AND ALWAYS ADDING USERS TO THE DATABASE
        loc = models.Location(city=form_sign_up.city.data, region=form_sign_up.region.data, country='placeholder')
        db.session.add(loc)
        #potentially uncomment this if you need to commit this before user
        #db.session.commit()
        flash('Sign up requested for user{}'.format(form_sign_up.username.data))
        user = models.User(username=form_sign_up.username.data, location_id=loc.id)
        user.set_password(form_sign_up.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect('/')
    return render_template('signup.html', title='Sign Up', form=form_sign_up)
