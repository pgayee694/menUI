from app import app, utils, session, view_models
from flask import render_template
import requests

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/menu-search', methods=['GET'])
def menu_search():
    id = find_loc_id('Omaha', 'Nebraska') #TODO: change this to get the current logged in user's location
    session['loc_id'] = id
    categories = utils.find_categories()
    cuisines = utils.find_cuisines(id)
    establishments = utils.find_establishments(id)
    return render_template('menu-search.html', title='Menu Search', categories=categories, cuisines=cuisines, establishments=establishments)

@app.route('/menu-browse', methods=['POST'])
def menu_browse():
    loc_id = session['loc_id']
    restaurant = request.form.get('restaurantName')
    category = request.form.getlist('category')
    cuisine = request.form.getlist('cuisine')
    establishment = request.form.getlist('establishment')

    cat_ids = None
    cu_ids = None
    establ_ids = None
    if category:
        cat_ids = utils.get_category_id(loc_id, category)
    if cuisine:
        cu_ids = utils.get_cuisine_id(loc_id, cuisine)
    if establishment:
        establ_ids = utils.get_establishment_id(loc_id, establishment)

    
