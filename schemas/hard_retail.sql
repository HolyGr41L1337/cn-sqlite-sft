CREATE TABLE brands (
  brand_id INTEGER PRIMARY KEY,
  brand_name TEXT NOT NULL,
  country TEXT,
  founded_year INTEGER
);
CREATE TABLE categories (
  category_id INTEGER PRIMARY KEY,
  category_name TEXT NOT NULL,
  parent_id INTEGER,
  level INTEGER
);
CREATE TABLE products (
  product_id INTEGER PRIMARY KEY,
  sku TEXT UNIQUE,
  product_name TEXT NOT NULL,
  brand_id INTEGER,
  category_id INTEGER,
  list_price REAL,
  cost_price REAL,
  launch_date TEXT,
  is_active INTEGER
);
CREATE TABLE warehouses (
  warehouse_id INTEGER PRIMARY KEY,
  warehouse_name TEXT,
  city TEXT,
  capacity INTEGER,
  open_date TEXT
);
CREATE TABLE inventory (
  inventory_id INTEGER PRIMARY KEY,
  product_id INTEGER,
  warehouse_id INTEGER,
  quantity INTEGER,
  safety_stock INTEGER,
  updated_at TEXT
);
CREATE TABLE suppliers (
  supplier_id INTEGER PRIMARY KEY,
  supplier_name TEXT,
  contact_city TEXT,
  rating REAL,
  cooperate_since TEXT
);
CREATE TABLE purchase_orders (
  po_id INTEGER PRIMARY KEY,
  supplier_id INTEGER,
  warehouse_id INTEGER,
  order_date TEXT,
  expected_date TEXT,
  status TEXT,
  total_amount REAL
);
CREATE TABLE purchase_items (
  item_id INTEGER PRIMARY KEY,
  po_id INTEGER,
  product_id INTEGER,
  quantity INTEGER,
  unit_cost REAL
);
CREATE TABLE customers (
  customer_id INTEGER PRIMARY KEY,
  customer_name TEXT,
  city TEXT,
  tier TEXT,
  register_date TEXT,
  birthday TEXT
);
CREATE TABLE sales_orders (
  order_id INTEGER PRIMARY KEY,
  customer_id INTEGER,
  order_time TEXT,
  channel TEXT,
  status TEXT,
  discount REAL,
  shipping_fee REAL
);
CREATE TABLE sales_items (
  item_id INTEGER PRIMARY KEY,
  order_id INTEGER,
  product_id INTEGER,
  quantity INTEGER,
  unit_price REAL,
  refunded INTEGER
);
CREATE TABLE returns (
  return_id INTEGER PRIMARY KEY,
  item_id INTEGER,
  return_date TEXT,
  quantity INTEGER,
  reason TEXT,
  refund_amount REAL
);
