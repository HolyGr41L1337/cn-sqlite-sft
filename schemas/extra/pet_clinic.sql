CREATE TABLE owner (id INTEGER PRIMARY KEY, full_name TEXT, phone TEXT, address TEXT);
CREATE TABLE pet (id INTEGER PRIMARY KEY, owner_id INTEGER, pet_name TEXT, species TEXT, birth_date TEXT);
CREATE TABLE veterinarian (id INTEGER PRIMARY KEY, full_name TEXT, license_no TEXT, hired_at TEXT);
CREATE TABLE visit (id INTEGER PRIMARY KEY, pet_id INTEGER, veterinarian_id INTEGER, visit_date TEXT, diagnosis TEXT, fee_amount REAL, status TEXT);
