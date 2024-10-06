from anytree import Node, RenderTree
from flask import Flask
from flask import redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from sqlalchemy.sql import text
from urllib.parse import unquote


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL").replace("s://", "sql://", 1)
db = SQLAlchemy(app)


@app.route("/")
def index():

    # fetch categories from database
    result = db.session.execute(text("SELECT id, category, parent FROM categories"))
    categories = result.fetchall()
    category_paths = build_trees_and_paths(categories)

    # fetch locations from database
    result = db.session.execute(text("SELECT id, location, parent FROM locations"))
    locations = result.fetchall()
    location_paths = build_trees_and_paths(locations)

    return render_template(
        "index.html",
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
    sql = text("INSERT INTO categories (category) VALUES (:category)")
    db.session.execute(sql, {"category":category})
    db.session.commit()
    return redirect("/")


@app.route("/add_location", methods=["POST"])
def add_location():
    location = request.form["location"]
    sql = text("INSERT INTO locations (location) VALUES (:location)")
    db.session.execute(sql, {"location":location})
    db.session.commit()
    return redirect("/")


@app.route('/add_subcategory/<int:category_id>', methods=['GET', 'POST'])
def add_subcategory(category_id):
    category_path = request.args.get('category_path')
    category_path = unquote(category_path)

    if request.method == 'POST':
        new_subcategory = request.form['new_subcategory']
        sql = text("INSERT INTO categories (category, parent) VALUES (:new_subcategory, :category_id)")
        db.session.execute(sql, {"new_subcategory":new_subcategory, "category_id":category_id})
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('add_subcategory.html', category_id=category_id, category_path=category_path)


@app.route('/add_sublocation/<int:location_id>', methods=['GET', 'POST'])
def add_sublocation(location_id):
    location_path = request.args.get('location_path')
    location_path = unquote(location_path)

    if request.method == 'POST':
        new_sublocation = request.form['new_sublocation']
        sql = text("INSERT INTO locations (location, parent) VALUES (:new_sublocation, :location_id)")
        db.session.execute(sql, {"new_sublocation":new_sublocation, "location_id":location_id})
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('add_sublocation.html', location_id=location_id, location_path=location_path)


def build_trees_and_paths(parent_list):
    print("polkujen generointi")
    nodes = {}  # Dictionary to store nodes by id

    for r in parent_list:
        print(r)

    # First pass: create nodes
    for id, name, parent_id in parent_list:
        nodes[id] = Node(name, id=id)

    # Second pass: attach parent-child relationships
    for id, name, parent_id in parent_list:
        if parent_id is not None:
            nodes[id].parent = nodes[parent_id]

    # print the tree structure
    roots = [node for node in nodes.values() if node.is_root]
    for root in roots:
        for pre, fill, node in RenderTree(root):
            print(f"{pre}{node.name} ({node.id})")

    # Build a list of category paths from root to each node
    category_paths = []
    for node in nodes.values():
        path = ": ".join([ancestor.name for ancestor in node.path])
        category_path = [node.id, path]
        category_paths.append(category_path)
    
    # Sort paths alphabetically
    category_paths.sort(key = lambda x: x[1].lower())
    print('\nPaths:')
    for p in category_paths:
        print(p)
    return category_paths