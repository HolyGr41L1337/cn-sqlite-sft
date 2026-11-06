CREATE TABLE warehouse (id INTEGER PRIMARY KEY, warehouse_name TEXT, city TEXT, capacity_kg REAL, opened_at TEXT);
CREATE TABLE courier (id INTEGER PRIMARY KEY, full_name TEXT, phone TEXT, warehouse_id INTEGER, hire_date TEXT, status TEXT);
CREATE TABLE shipment (id INTEGER PRIMARY KEY, tracking_no TEXT, order_date TEXT, weight_kg REAL, freight_fee REAL, status TEXT, courier_id INTEGER);
CREATE TABLE shipment_event (id INTEGER PRIMARY KEY, shipment_id INTEGER, event_time TEXT, location TEXT, event_note TEXT);
