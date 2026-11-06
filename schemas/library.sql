CREATE TABLE books (
  book_id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  author TEXT,
  category TEXT,
  publish_year INTEGER,
  price REAL,
  total_copies INTEGER
);
CREATE TABLE readers (
  reader_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  gender TEXT,
  register_date TEXT,
  reader_type TEXT,
  phone TEXT
);
CREATE TABLE borrows (
  borrow_id INTEGER PRIMARY KEY,
  book_id INTEGER,
  reader_id INTEGER,
  borrow_date TEXT,
  due_date TEXT,
  return_date TEXT,
  fine REAL
);
CREATE TABLE staff (
  staff_id INTEGER PRIMARY KEY,
  name TEXT,
  position TEXT,
  hire_date TEXT,
  salary REAL
);
