from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL").replace("s://", "sql://", 1)
db = SQLAlchemy(app)




# User accounts


def add_user(username, password, role='user'):
    hash_value = generate_password_hash(password)
    sql = text("INSERT INTO users (username, password, role) VALUES (:username, :password, :role)")
    db.session.execute(sql, {"username":username, "password":hash_value, "role":role} )
    db.session.commit()


def check_password(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if not user: # invalid username
        return None
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            return True
        else:
            return False




# Categories and locations


def get_categories():
    result = db.session.execute(text("SELECT id, category, parent FROM categories"))
    return result.fetchall()


def get_locations():
    result = db.session.execute(text("SELECT id, location, parent FROM locations"))
    return result.fetchall()


def add_category(category_name):
    sql = text("INSERT INTO categories (category) VALUES (:category_name)")
    db.session.execute(sql, {"category_name":category_name})
    db.session.commit()


def add_subcategory(category_name, parent_id):
    sql = text("INSERT INTO categories (category, parent) VALUES (:new_subcategory, :category_id)")
    db.session.execute(sql, {"new_subcategory":category_name, "category_id":parent_id})
    db.session.commit()


def add_location(location_name):
    sql = text("INSERT INTO locations (location) VALUES (:location_name)")
    db.session.execute(sql, {"location_name":location_name})
    db.session.commit()


def add_sublocation(location_name, parent_id):
    sql = text("INSERT INTO locations (location, parent) VALUES (:new_sublocation, :location_id)")
    db.session.execute(sql, {"new_sublocation":location_name, "location_id":parent_id})
    db.session.commit()


