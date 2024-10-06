from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from sqlalchemy.sql import text

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL").replace("s://", "sql://", 1)
db = SQLAlchemy(app)


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
