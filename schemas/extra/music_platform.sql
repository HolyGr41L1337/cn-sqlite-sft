CREATE TABLE artist (id INTEGER PRIMARY KEY, artist_name TEXT, genre TEXT, debut_date TEXT);
CREATE TABLE album (id INTEGER PRIMARY KEY, artist_id INTEGER, album_title TEXT, release_date TEXT, price REAL);
CREATE TABLE listener (id INTEGER PRIMARY KEY, username TEXT, email TEXT, subscribed_at TEXT, status TEXT);
CREATE TABLE subscription (id INTEGER PRIMARY KEY, listener_id INTEGER, album_id INTEGER, started_at TEXT, monthly_fee REAL, status TEXT);
