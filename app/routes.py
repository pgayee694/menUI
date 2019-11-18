from app import app, utils, view_models, models, db
from flask import Flask, render_template, flash, redirect, session, request
import requests
from app.forms import LoginForm, SignInForm
from .models import db, User, Location
from flask_login import login_user, current_user

@app.route('/')
def hello():
    return render_template('home.html', title='Home')

@app.route('/menu-search', methods=['GET'])
def menu_search():
    id = utils.find_loc_id('Omaha', 'Nebraska') #TODO: change this to get the current logged in user's location
    session['loc_id'] = id
    categories = utils.find_categories()
    cuisines = utils.find_cuisines(id)
    establishments = utils.find_establishments(id)
    return render_template('menu-search.html', title='Menu Search', categories=categories, cuisines=cuisines, establishments=establishments)

@app.route('/menu-browse', methods=['POST'])
def menu_browse():
    loc_id = session['loc_id']
    res_name = request.form.get('restaurantName') or ''
    category = request.form.getlist('category')
    cuisine = request.form.getlist('cuisine')
    establishment = request.form.getlist('establishment')
    
    cat_ids = None
    cu_ids = None
    establ_ids = None
    if category:
        cat_ids = utils.get_category_id(category)
    if cuisine:
        cu_ids = utils.get_cuisine_id(loc_id, cuisine)
    if establishment:
        establ_ids = utils.get_establishment_id(loc_id, establishment)

    res_ids = utils.search_restaurants(loc_id, cat_ids, cu_ids, establ_ids)

    restaurants = []
    for res_id in res_ids:
        restaurants.append(utils.get_restaurant_details(res_id))

    valid_restaurants = [restaurant for restaurant in restaurants if res_name in restaurant.name]
    return render_template('menu-browse.html', restaurants=valid_restaurants, isAdd=True)

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
            return redirect('/login/')
        login_user(user, remember=form_log_in.remember_me.data)
        return redirect('/')
    return render_template('login.html', title='Log In', form=form_log_in)

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    form_sign_up = SignInForm()
    if form_sign_up.validate_on_submit() and form_sign_up.password.data == form_sign_up.password2.data:
        #before creating a location query database and see if it exists already
        db.create_all()
        #CURRENTLY THIS IS DOING NO VALIDATION AND ALWAYS ADDING USERS TO THE DATABASE
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
