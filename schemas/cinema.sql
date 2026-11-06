CREATE TABLE movies (
  movie_id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  genre TEXT,
  release_date TEXT,
  duration_minutes INTEGER,
  rating REAL
);
CREATE TABLE halls (
  hall_id INTEGER PRIMARY KEY,
  hall_name TEXT,
  capacity INTEGER,
  screen_type TEXT
);
CREATE TABLE screenings (
  screening_id INTEGER PRIMARY KEY,
  movie_id INTEGER,
  hall_id INTEGER,
  start_time TEXT,
  end_time TEXT,
  price REAL
);
CREATE TABLE tickets (
  ticket_id INTEGER PRIMARY KEY,
  screening_id INTEGER,
  seat_no TEXT,
  buyer_phone TEXT,
  sold_at TEXT,
  price REAL
);
CREATE TABLE members (
  member_id INTEGER PRIMARY KEY,
  name TEXT,
  phone TEXT,
  join_date TEXT,
  points INTEGER
);
