CREATE TABLE departments (
  dept_id INTEGER PRIMARY KEY,
  dept_name TEXT NOT NULL,
  city TEXT,
  budget REAL
);
CREATE TABLE employees (
  emp_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  dept_id INTEGER,
  position TEXT,
  hire_date TEXT,
  salary REAL,
  manager_id INTEGER
);
CREATE TABLE projects (
  project_id INTEGER PRIMARY KEY,
  project_name TEXT NOT NULL,
  dept_id INTEGER,
  start_date TEXT,
  end_date TEXT,
  budget REAL
);
CREATE TABLE project_members (
  id INTEGER PRIMARY KEY,
  project_id INTEGER,
  emp_id INTEGER,
  role TEXT,
  hours INTEGER
);
CREATE TABLE salaries (
  id INTEGER PRIMARY KEY,
  emp_id INTEGER,
  month TEXT,
  base REAL,
  bonus REAL
);
