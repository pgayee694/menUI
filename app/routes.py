from app import app, utils, view_models, models, db, scraper
from flask import Flask, render_template, flash, redirect, session, request
import requests
import time
import sys
from app.forms import LoginForm, SignInForm, FriendForm
from .models import db, User, Location
from flask_login import login_user, current_user, logout_user
import time

@app.route('/')
def hello():
    return render_template('home.html', title='Home')

@app.route('/borgar')
def borgar():
    return render_template('borgar.html', title='borgar')

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

@app.route('/menu-browse', methods=['GET', 'POST'])
def menu_browse():
    if not current_user.is_authenticated:
        return redirect('/login')

    if request.method == 'POST':
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
    else:
        #GET
        start = time.time()

        res_names = utils.get_user_restaurants(current_user.id)
        loc_id = session['loc_id']
        
        sess = requests.Session()
        res_ids = []
        for res_name in res_names:
            res_ids += utils.search_restaurants(loc_id, res_name, [], [], [], sess)
        
        restaurants = utils.get_restaurant_details(res_ids)

        valids = [r for r in restaurants if r.name in res_names]

        return render_template('menu-browse.html', restaurants=valids, isAdd=False)

@app.route('/menu-compare', methods=['GET'])
def menu_compare():
    if not current_user.is_authenticated:
        return redirect('/login')
    users = utils.get_friendlist(current_user.id)
    title = 'Compare with Friends Lists'

    if request.form.get('union'):
        #TODO Test Union with users that actually have restaurant lists
        users.append(current_user)
        restaurant_ids = utils.union_restaurants(users)
        restaurants = utils.get_restaurant_details(restaurant_ids)
        return render_template('menu-browse.html', restaurants=restaurants, isAdd=False)

    if request.form.get('intersection'):
        #TODO Test Intersection with users that actually have restaurant lists
        users.append(current_user)
        restaurant_ids = utils.intersection_restaurants(users)
        restaurants = utils.get_restaurant_details(restaurant_ids)
        return render_template('menu-browse.html', restaurants=restaurants, isAdd=False)

    return render_template('menu-compare.html', title=title, users=users)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form_log_in = LoginForm()
    if current_user.is_authenticated:
        return redirect('/')

    if form_log_in.validate_on_submit():
        user = utils.find_user_by_username(form_log_in.username.data)
        if user is None or not user.check_password(form_log_in.password.data):
            flash('Invalid username or password, try again.')
            return render_template('login.html', title='Log In', form=form_log_in)


        login_user(user, remember=form_log_in.remember_me.data)
        return redirect('/')

    return render_template('login.html', title='Log In', form=form_log_in)

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    form_sign_up = SignInForm()
    if current_user.is_authenticated:
        return redirect('/')

    if utils.find_user_by_username(form_sign_up.username.data):
        flash('That username is taken, please try again.')
        return render_template('signup.html', title='Sign Up', form=form_sign_up)

    if form_sign_up.password.data != form_sign_up.password2.data:
        flash("Your passwords didn't match, please try again.")
        return render_template('signup.html', title='Sign Up', form=form_sign_up)

    if form_sign_up.validate_on_submit() and form_sign_up.password.data == form_sign_up.password2.data:
        db.create_all()
        loc = None
        locID = models.Location.query.filter_by(city=form_sign_up.city.data, region=form_sign_up.region.data).first().id
        if not locID:
            loc = models.Location(city=form_sign_up.city.data, region=form_sign_up.region.data, country='placeholder', id = locID)
            db.session.add(loc)
            db.session.commit()
        else:
            loc = models.Location(city=form_sign_up.city.data, region=form_sign_up.region.data, country='placeholder')

        
        user = models.User(username=form_sign_up.username.data, location_id=loc.id)
        user.set_password(form_sign_up.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect('/login/')

    return render_template('signup.html', title='Sign Up', form=form_sign_up)

@app.route('/friends/', methods=['GET', 'POST'])
def friends():
    form_friends = FriendForm()
    if not current_user.is_authenticated:
        return redirect('/login/')

    if not form_friends.username.data:
        return render_template('friends.html', title='Connect With Friends', form=form_friends)

    if form_friends.username.data == current_user.username:
        # user tried to add themself as a friend
        flash('Feeling desperate?')
        return render_template('friends.html', title='Connect With Friends', form=form_friends)

    if not utils.find_user_by_username(form_friends.username.data) and form_friends.username.data:
        # This message is currently displayed be defualt, it shouldn't be.
        flash('User not found.')
        return render_template('friends.html', title='Connect With Friends', form=form_friends)

    friend1 = utils.find_user_by_username(current_user.username)
    friend2 = utils.find_user_by_username(form_friends.username.data)
    if utils.find_friendship(friend1.id, friend2.id):
        flash("You already have that friend.")
        return render_template('friends.html', title='Connect With Friends', form=form_friends)

    friendship = models.Friends(friend1_id=friend1.id, friend2_id=friend2.id)
    db.session.add(friendship)
    db.session.commit()
    flash('Friend added successfully!')
    return render_template('friends.html', title='Connect With Friends', form=form_friends)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/')
	
@app.route('/menu-add', methods=['GET', 'POST'])
def menu_add():
	
	utils.add_user_restaurant(current_user.id, request.form.get('add'))
	flash("Restaurant " + request.form.get('add') + " was added!!!")
	
	return redirect('/')

@app.route('/menu-details', methods=['POST'])
def menu_details():
    menurl = request.form.get('menurl')
    
    menu_items = scraper.parse_zomato(menurl) if 'zomato' in menurl else []
    return render_template('menu-details.html', title='Menu Details', items=menu_items, isImage='Page' in menu_items[0].name)