CREATE TABLE customers (
  customer_id INTEGER PRIMARY KEY,
  name TEXT,
  city TEXT,
  register_date TEXT,
  level TEXT
);
CREATE TABLE products (
  product_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  category TEXT,
  price REAL,
  stock INTEGER
);
CREATE TABLE orders (
  order_id INTEGER PRIMARY KEY,
  customer_id INTEGER,
  order_date TEXT,
  status TEXT,
  total_amount REAL
);
CREATE TABLE order_items (
  item_id INTEGER PRIMARY KEY,
  order_id INTEGER,
  product_id INTEGER,
  quantity INTEGER,
  unit_price REAL
);
CREATE TABLE payments (
  payment_id INTEGER PRIMARY KEY,
  order_id INTEGER,
  pay_method TEXT,
  pay_time TEXT,
  amount REAL
);
