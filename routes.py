from flask import redirect, render_template, request, session, url_for
from sqlalchemy.sql import text
from urllib.parse import unquote

from data_structures import build_paths_and_trees
from app import app
import db


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # TODO: check username and password
    session["username"] = username
    return redirect("/results")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/results")
def results():
    categories = db.get_categories()
    category_paths = build_paths_and_trees(categories)

    locations = db.get_locations()
    location_paths = build_paths_and_trees(locations)

    return render_template(
        "results.html",
        category_count=len(category_paths),
        categories=category_paths,
        location_count=len(location_paths),
        locations=location_paths
    ) 


@app.route("/new_category")
def new_category():
    return render_template("new_category.html")


@app.route("/new_location")
def new_location():
    return render_template("new_location.html")


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
