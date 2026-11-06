CREATE TABLE facility (id INTEGER PRIMARY KEY, facility_name TEXT, city TEXT, capacity_m3 REAL, opened_date TEXT);
CREATE TABLE client (id INTEGER PRIMARY KEY, client_name TEXT, contact_phone TEXT, onboard_date TEXT, status TEXT);
CREATE TABLE slot (id INTEGER PRIMARY KEY, facility_id INTEGER, slot_code TEXT, temperature_zone TEXT, monthly_rate REAL, status TEXT);
CREATE TABLE lease (id INTEGER PRIMARY KEY, slot_id INTEGER, client_id INTEGER, start_date TEXT, end_date TEXT, monthly_fee REAL, status TEXT);
