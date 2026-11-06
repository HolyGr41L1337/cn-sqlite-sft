CREATE TABLE company (id INTEGER PRIMARY KEY, company_name TEXT, industry TEXT, city TEXT, created_date TEXT);
CREATE TABLE job (id INTEGER PRIMARY KEY, company_id INTEGER, title TEXT, salary_min REAL, salary_max REAL, posted_date TEXT, status TEXT);
CREATE TABLE candidate (id INTEGER PRIMARY KEY, full_name TEXT, email TEXT, resume_url TEXT, registered_date TEXT);
CREATE TABLE application (id INTEGER PRIMARY KEY, job_id INTEGER, candidate_id INTEGER, applied_date TEXT, stage TEXT);
