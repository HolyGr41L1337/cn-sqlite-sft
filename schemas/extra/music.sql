CREATE TABLE artist (id INTEGER PRIMARY KEY, artist_name TEXT, country TEXT, debut_date TEXT);
CREATE TABLE album (id INTEGER PRIMARY KEY, artist_id INTEGER, album_title TEXT, release_date TEXT, price REAL);
CREATE TABLE listener (id INTEGER PRIMARY KEY, nickname TEXT, email TEXT, signup_date TEXT, status TEXT);
CREATE TABLE subscription (id INTEGER PRIMARY KEY, listener_id INTEGER, album_id INTEGER, subscribed_date TEXT, paid_amount REAL, status TEXT);
