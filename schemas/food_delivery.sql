CREATE TABLE restaurants (
  restaurant_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  city TEXT,
  category TEXT,
  rating REAL,
  open_date TEXT
);
CREATE TABLE dishes (
  dish_id INTEGER PRIMARY KEY,
  restaurant_id INTEGER,
  name TEXT NOT NULL,
  price REAL,
  month_sales INTEGER
);
CREATE TABLE riders (
  rider_id INTEGER PRIMARY KEY,
  name TEXT,
  city TEXT,
  join_date TEXT,
  rating REAL
);
CREATE TABLE orders (
  order_id INTEGER PRIMARY KEY,
  restaurant_id INTEGER,
  rider_id INTEGER,
  customer_phone TEXT,
  order_time TEXT,
  amount REAL,
  status TEXT
);
CREATE TABLE complaints (
  complaint_id INTEGER PRIMARY KEY,
  order_id INTEGER,
  reason TEXT,
  handle_status TEXT,
  created_at TEXT
);
