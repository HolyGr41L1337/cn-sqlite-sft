CREATE TABLE supplier (id INTEGER PRIMARY KEY, supplier_name TEXT, contact_phone TEXT, country TEXT);
CREATE TABLE product (id INTEGER PRIMARY KEY, supplier_id INTEGER, sku TEXT, product_name TEXT, unit_price REAL);
CREATE TABLE stock_item (id INTEGER PRIMARY KEY, product_id INTEGER, bin_location TEXT, quantity_on_hand INTEGER, last_counted_at TEXT);
CREATE TABLE stock_movement (id INTEGER PRIMARY KEY, stock_item_id INTEGER, moved_at TEXT, quantity_change INTEGER, movement_type TEXT, status TEXT);
