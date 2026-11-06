CREATE TABLE company (id INTEGER PRIMARY KEY, company_name TEXT, industry TEXT, city TEXT, registered_at TEXT);
CREATE TABLE job_posting (id INTEGER PRIMARY KEY, company_id INTEGER, job_title TEXT, salary_min REAL, salary_max REAL, posted_at TEXT, status TEXT);
CREATE TABLE candidate (id INTEGER PRIMARY KEY, full_name TEXT, email TEXT, years_experience INTEGER, created_at TEXT);
CREATE TABLE application (id INTEGER PRIMARY KEY, job_posting_id INTEGER, candidate_id INTEGER, applied_at TEXT, expected_salary REAL, status TEXT);
