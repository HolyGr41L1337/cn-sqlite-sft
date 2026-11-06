CREATE TABLE member (id INTEGER PRIMARY KEY, full_name TEXT, phone TEXT, join_date TEXT, status TEXT);
CREATE TABLE trainer (id INTEGER PRIMARY KEY, full_name TEXT, specialty TEXT, hourly_rate REAL);
CREATE TABLE class_session (id INTEGER PRIMARY KEY, trainer_id INTEGER, class_name TEXT, start_time TEXT, duration_min INTEGER, fee REAL);
CREATE TABLE attendance (id INTEGER PRIMARY KEY, member_id INTEGER, class_session_id INTEGER, attended_at TEXT, paid_amount REAL);
