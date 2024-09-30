from anytree import Node, RenderTree
from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from sqlalchemy.sql import text

app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
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
            print("%s%s" % (pre, node.name))

    paths = []
    for node in nodes.values():
        path = ": ".join([ancestor.name for ancestor in node.path])  # Build path from root to current node
        paths.append(path)
    
    # Sort paths alphabetically
    paths.sort()
    print('\nPaths:')
    for p in paths:
        print(p)
    return paths