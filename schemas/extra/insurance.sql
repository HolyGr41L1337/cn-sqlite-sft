CREATE TABLE policyholder (id INTEGER PRIMARY KEY, full_name TEXT, id_number TEXT, registered_at TEXT);
CREATE TABLE policy (id INTEGER PRIMARY KEY, policyholder_id INTEGER, policy_type TEXT, premium_amount REAL, effective_date TEXT, status TEXT);
CREATE TABLE claim (id INTEGER PRIMARY KEY, policy_id INTEGER, filed_at TEXT, claim_amount REAL, approved_amount REAL, status TEXT);
CREATE TABLE agent (id INTEGER PRIMARY KEY, full_name TEXT, region TEXT, hire_date TEXT);
