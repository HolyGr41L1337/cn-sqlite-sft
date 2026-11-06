CREATE TABLE instructor (id INTEGER PRIMARY KEY, full_name TEXT, expertise TEXT, joined_at TEXT);
CREATE TABLE course (id INTEGER PRIMARY KEY, instructor_id INTEGER, title TEXT, price REAL, published_at TEXT, status TEXT);
CREATE TABLE student (id INTEGER PRIMARY KEY, full_name TEXT, email TEXT, signup_date TEXT);
CREATE TABLE enrollment (id INTEGER PRIMARY KEY, student_id INTEGER, course_id INTEGER, enrolled_at TEXT, progress_percent INTEGER, paid_amount REAL);
