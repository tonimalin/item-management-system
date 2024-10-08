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
