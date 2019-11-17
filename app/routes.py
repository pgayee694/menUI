from app import app
from flask import render_template

@app.route('/')
def hello():
    return 'Hello, World!'
	
@app.route('/menu-search', methods=['GET'])
def menu_search():
        return render_template('menu-search.html',
		title='Menu Search')
		
@app.route('/menu-browse', methods=['GET'])
def menu_browse():
        return render_template('menu-browse.html',
		title='Menu Browse')