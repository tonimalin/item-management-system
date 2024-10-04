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
    result = db.session.execute(text("SELECT id, category, parent FROM categories"))
    categories = result.fetchall()
    paths = build_trees_and_paths(categories)
    return render_template("index.html", count=len(paths), categories=paths) 


@app.route("/new")
def new():
    return render_template("new.html")


@app.route("/send", methods=["POST"])
def send():
    category = request.form["category"]
    sql = text("INSERT INTO categories (category) VALUES (:category)")
    db.session.execute(sql, {"category":category})
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
    category_paths.sort(key = lambda x: x[1])
    print('\nPaths:')
    for p in category_paths:
        print(p)
    return category_paths