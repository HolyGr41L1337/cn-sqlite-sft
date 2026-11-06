CREATE TABLE venue (id INTEGER PRIMARY KEY, venue_name TEXT, city TEXT, seat_capacity INTEGER);
CREATE TABLE event (id INTEGER PRIMARY KEY, venue_id INTEGER, event_name TEXT, event_date TEXT, base_price REAL, status TEXT);
CREATE TABLE buyer (id INTEGER PRIMARY KEY, full_name TEXT, email TEXT, registered_at TEXT);
CREATE TABLE ticket_order (id INTEGER PRIMARY KEY, event_id INTEGER, buyer_id INTEGER, seat_no TEXT, order_time TEXT, amount REAL, status TEXT);
