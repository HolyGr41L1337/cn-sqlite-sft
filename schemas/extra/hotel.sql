CREATE TABLE guest (id INTEGER PRIMARY KEY, full_name TEXT, email TEXT, membership_level TEXT, registered_at TEXT);
CREATE TABLE room (id INTEGER PRIMARY KEY, room_number TEXT, room_type TEXT, nightly_rate REAL, floor_number INTEGER, status TEXT);
CREATE TABLE reservation (id INTEGER PRIMARY KEY, guest_id INTEGER, room_id INTEGER, check_in_date TEXT, check_out_date TEXT, total_amount REAL, status TEXT);
CREATE TABLE payment (id INTEGER PRIMARY KEY, reservation_id INTEGER, paid_at TEXT, amount REAL, method TEXT);
