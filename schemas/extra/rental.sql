CREATE TABLE landlord (id INTEGER PRIMARY KEY, full_name TEXT, phone TEXT, joined_at TEXT);
CREATE TABLE apartment (id INTEGER PRIMARY KEY, landlord_id INTEGER, address TEXT, monthly_rent REAL, bedroom_count INTEGER, status TEXT);
CREATE TABLE tenant (id INTEGER PRIMARY KEY, full_name TEXT, email TEXT, created_at TEXT);
CREATE TABLE lease (id INTEGER PRIMARY KEY, apartment_id INTEGER, tenant_id INTEGER, start_date TEXT, end_date TEXT, deposit_amount REAL, status TEXT);
