CREATE TABLE students (
  student_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  gender TEXT,
  birth_date TEXT,
  class_id INTEGER,
  enrollment_year INTEGER
);
CREATE TABLE classes (
  class_id INTEGER PRIMARY KEY,
  class_name TEXT NOT NULL,
  grade INTEGER,
  head_teacher TEXT
);
CREATE TABLE teachers (
  teacher_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  subject TEXT,
  hire_date TEXT,
  salary REAL
);
CREATE TABLE courses (
  course_id INTEGER PRIMARY KEY,
  course_name TEXT NOT NULL,
  teacher_id INTEGER,
  credit REAL,
  hours INTEGER
);
CREATE TABLE scores (
  score_id INTEGER PRIMARY KEY,
  student_id INTEGER,
  course_id INTEGER,
  score REAL,
  exam_date TEXT
);
