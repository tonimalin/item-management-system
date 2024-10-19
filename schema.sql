CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    category TEXT NOT NULL,
    parent INTEGER REFERENCES categories(id) ON DELETE SET NULL
);

CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    location TEXT NOT NULL,
    parent INTEGER REFERENCES locations(id) ON DELETE SET NULL
);

CREATE TABLE item_locations (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    location_id INTEGER REFERENCES locations(id) ON DELETE SET NULL,
    notes TEXT
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    task TEXT,
    owner_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    status TEXT,
    notes TEXT,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    location_id INTEGER REFERENCES locations(id) ON DELETE SET NULL,
    item_location_id INTEGER REFERENCES item_locations(id) ON DELETE SET NULL
);
