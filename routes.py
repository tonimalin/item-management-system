from flask import redirect, render_template, request, session, url_for
from sqlalchemy.sql import text
from urllib.parse import unquote

from data_structures import build_paths_and_trees
from app import app
import db




# User account routes


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if db.check_password(username, password):
        session["username"] = username
        return redirect("/results")
    else:
        return('Virheellinen tunnus tai salasana!')


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/new_user")
def new_user():
    return render_template("new_user.html")


@app.route("/add_user", methods=["POST"])
def add_user():
    username = request.form["username"]
    password = request.form["password"]
    if db.check_password(username, password) == None:
        if password == '':
            return("Salasana ei saa olla tyhjä!")
        db.add_user(username, password, 'user')
        return(f"Luotiin käyttäjä: {username}")
    else:
        return(f"Tunnus <b>{username}</b> on jo käytössä!")




# Other routes


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/results")
def results():

    # if general filter is activated then others filters are disabled
    # if category, location or item location filter is activated
    #     then general filter is disabled

    if request.method == 'GET':

        # General filter
        if 'general' in request.args:
            session['general'] = request.args.get('general')
            session.pop('category', None)
            session.pop('location', None)
            session.pop('item_location', None)
            session['active_filter'] = 'general'
        
        # Category filter
        elif 'category' in request.args:
            session['category'] = request.args.get('category')
            session.pop('general', None)
            session['active_filter'] = 'category'

        # Location filter
        elif 'location' in request.args:
            session['location'] = request.args.get('location')
            session.pop('general', None)
            session['active_filter'] = 'location'

        # Item Location filter
        elif 'item_location' in request.args:
            session['item_location'] = request.args.get('item_location')
            session.pop('general', None)
            session['active_filter'] = 'item_location'

        if 'submit' in request.args:
            if request.args.get('submit') == 'Tyhjennä kaikki suodattimet':
                session.pop('general', None)
                session.pop('category', None)
                session.pop('location', None)
                session.pop('item_location', None)
            if request.args.get('submit') == 'Tyhjennä kategoriasuodatin':
                session.pop('category', None)
            if request.args.get('submit') == 'Tyhjennä paikkasuodatin':
                session.pop('location', None)
            if request.args.get('submit') == 'Tyhjennä tavaran sijaintisuodatin':
                session.pop('item_location', None)
                

    # strings that are used to filter categories, locations and item locations
    filter_strings = 3 * ['']
    if 'general' in session:
            filter_strings = 3 * [session['general']]
    else:
        for i,l in enumerate(['category', 'location', 'item_location']):
            if l in session:
                filter_strings[i] = session[l]

    categories = db.get_categories()
    category_paths = build_paths_and_trees(categories)
    locations = db.get_locations()
    location_paths = build_paths_and_trees(locations)

    if 'category' in session or 'general' in session:
        category_paths = [
            path for path in category_paths
                if filter_strings[0].lower() in path[1].lower()
        ]
    if 'location' in session or 'general' in session:
        location_paths = [
            path for path in location_paths
                if filter_strings[1].lower() in path[1].lower()
        ]
    if 'item_location' in session:
        pass

    return render_template(
        "results.html",
        category_count=len(category_paths),
        categories=category_paths,
        location_count=len(location_paths),
        locations=location_paths,
    ) 


@app.route("/new_category")
def new_category():
    return render_template("new_category.html")


@app.route("/new_location")
def new_location():
    return render_template("new_location.html")


@app.route("/new_item_location")
def new_item_location():
    return render_template("new_item_location.html")


@app.route("/add_category", methods=["POST"])
def add_category():
    category = request.form["category"]
    db.add_category(category)
    return redirect("/results")


@app.route("/add_location", methods=["POST"])
def add_location():
    location = request.form["location"]
    db.add_location(location)
    return redirect("/results")


@app.route('/add_subcategory/<int:category_id>', methods=['GET', 'POST'])
def add_subcategory(category_id):
    category_path = request.args.get('category_path')
    category_path = unquote(category_path)

    if request.method == 'POST':
        new_subcategory = request.form['new_subcategory']
        db.add_subcategory(new_subcategory, category_id)
        return redirect(url_for('results'))
    
    return render_template('add_subcategory.html', category_id=category_id, category_path=category_path)


@app.route('/add_sublocation/<int:location_id>', methods=['GET', 'POST'])
def add_sublocation(location_id):
    location_path = request.args.get('location_path')
    location_path = unquote(location_path)

    if request.method == 'POST':
        new_sublocation = request.form['new_sublocation']
        db.add_sublocation(new_sublocation, location_id)
        return redirect(url_for('results'))
    
    return render_template('add_sublocation.html', location_id=location_id, location_path=location_path)
