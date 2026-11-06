CREATE TABLE members (
  member_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  gender TEXT,
  join_date TEXT,
  member_level TEXT,
  phone TEXT,
  expire_date TEXT
);
CREATE TABLE coaches (
  coach_id INTEGER PRIMARY KEY,
  name TEXT,
  specialty TEXT,
  hire_date TEXT,
  salary REAL
);
CREATE TABLE classes (
  class_id INTEGER PRIMARY KEY,
  class_name TEXT NOT NULL,
  coach_id INTEGER,
  duration_minutes INTEGER,
  price REAL,
  capacity INTEGER
);
CREATE TABLE bookings (
  booking_id INTEGER PRIMARY KEY,
  member_id INTEGER,
  class_id INTEGER,
  booking_time TEXT,
  status TEXT,
  paid_amount REAL
);
CREATE TABLE checkins (
  checkin_id INTEGER PRIMARY KEY,
  member_id INTEGER,
  checkin_time TEXT,
  device TEXT
);
