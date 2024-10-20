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


# def get_categories():
#     result = db.session.execute(text("SELECT id, category, parent FROM categories"))
#     return result.fetchall()

def get_categories(id=None, category_substring=None):

    # "WHERE true" allows flexible addition of AND clauses
    sql = "SELECT id, category, parent FROM categories WHERE true"
    params = {}
    
    # Add filtering by id if provided
    if id:
        sql += " AND id = :id"
        params["id"] = id
    
    # Add filtering by category substring if provided
    if category_substring:
        sql += " AND category ILIKE :category_substring"
        params["category_substring"] = f"%{category_substring}%"

    result = db.session.execute(text(sql), params)
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




# Item Locations


def add_item_location(category_id=None, location_id=None, notes=None):

    # category or location of items must be known
    if category_id == None and location_id == None:
        return None
    
    # tarkistetaan, että category ja location on olemassa
    # tarkistetaan, että category tai location on annettu
        # miten virhe käsitellään?
            # palauttaa None jos ei lisätty mitään ja id:n jos lisättiin?
    pass