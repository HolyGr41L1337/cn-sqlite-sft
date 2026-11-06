CREATE TABLE customer (id INTEGER PRIMARY KEY, full_name TEXT, id_number TEXT, phone TEXT, created_at TEXT);
CREATE TABLE account (id INTEGER PRIMARY KEY, customer_id INTEGER, account_no TEXT, account_type TEXT, balance REAL, status TEXT, opened_at TEXT);
CREATE TABLE transaction_record (id INTEGER PRIMARY KEY, account_id INTEGER, txn_time TEXT, amount REAL, direction TEXT, memo TEXT);
CREATE TABLE loan (id INTEGER PRIMARY KEY, customer_id INTEGER, principal REAL, interest_rate REAL, start_date TEXT, status TEXT);
