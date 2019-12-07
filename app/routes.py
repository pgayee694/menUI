from app import app, utils, view_models, models, db
from flask import Flask, render_template, flash, redirect, session, request
import requests
import time
import sys
from app.forms import LoginForm, SignInForm
from .models import db, User, Location
from flask_login import login_user, current_user, logout_user

@app.route('/')
def hello():
    return render_template('home.html', title='Home')

@app.route('/menu-search', methods=['GET'])
def menu_search():
    if not current_user.is_authenticated:
        return redirect('/login')
    location = models.Location.query.filter_by(id=current_user._get_current_object().location_id).first()
    id = utils.find_loc_id(location.city, location.region)
    session['loc_id'] = id
    categories = utils.find_categories()
    session['categories'] = categories
    cuisines = utils.find_cuisines(id)
    session['cuisines'] = cuisines
    establishments = utils.find_establishments(id)
    session['establs'] = establishments
    return render_template('menu-search.html', title='Menu Search', categories=categories.keys(), cuisines=cuisines.keys(), establishments=establishments.keys())

@app.route('/menu-browse', methods=['POST'])
def menu_browse():
    if not current_user.is_authenticated:
        return redirect('/login')
    loc_id = session['loc_id']
    res_name = request.form.get('restaurantName') or ''
    category = request.form.getlist('category')
    cuisine = request.form.getlist('cuisine')
    establishment = request.form.getlist('establishment')
    
    cats = session['categories']
    cus = session['cuisines']
    establs = session['establs']

    cat_ids = [cats[cat] for cat in category]
    cu_ids = [cus[c] for c in cuisine]
    establ_ids = [establs[establ] for establ in establishment]

    res_ids = utils.search_restaurants(loc_id, res_name, cat_ids, cu_ids, establ_ids)
    restaurants = utils.get_restaurant_details(res_ids)

    return render_template('menu-browse.html', restaurants=restaurants, isAdd=True)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form_log_in = LoginForm()
    if current_user.is_authenticated:
        return redirect('/')
    if form_log_in.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form_log_in.username.data, form_log_in.remember_me.data))
        user = models.User.query.filter_by(username=form_log_in.username.data).first()
        if user is None or not user.check_password(form_log_in.password.data):
            flash('invalid username or password')
            return render_template('login.html', title='Log In', form=form_log_in, invalid=True)
        login_user(user, remember=form_log_in.remember_me.data)
        return redirect('/')
    return render_template('login.html', title='Log In', form=form_log_in)

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    form_sign_up = SignInForm()
    if current_user.is_authenticated:
        return redirect('/')
    user = models.User.query.filter_by(username=form_sign_up.username.data).first()
    if not(user is None):
        return render_template('signup.html', title='Sign Up', form=form_sign_up, user_exists=True)
    if not(form_sign_up.password.data == form_sign_up.password2.data):
        return render_template('signup.html', title='Sign Up', form=form_sign_up, no_match=True)
    if form_sign_up.validate_on_submit() and form_sign_up.password.data == form_sign_up.password2.data:
        #before creating a location query database and see if it exists already
        db.create_all()
        #TODO: CURRENTLY THIS IS DOING NO VALIDATION AND ALWAYS ADDING USERS TO THE DATABASE
        loc = models.Location(city=form_sign_up.city.data, region=form_sign_up.region.data, country='placeholder')
        db.session.add(loc)
        db.session.commit()
        flash('Sign up requested for user{}'.format(form_sign_up.username.data))
        user = models.User(username=form_sign_up.username.data, location_id=loc.id)
        user.set_password(form_sign_up.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect('/login/')
    return render_template('signup.html', title='Sign Up', form=form_sign_up)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/')