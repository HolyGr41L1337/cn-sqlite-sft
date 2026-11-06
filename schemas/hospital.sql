CREATE TABLE patients (
  patient_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  gender TEXT,
  birth_date TEXT,
  phone TEXT,
  insurance_type TEXT
);
CREATE TABLE doctors (
  doctor_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  department TEXT,
  title TEXT,
  join_date TEXT
);
CREATE TABLE appointments (
  appointment_id INTEGER PRIMARY KEY,
  patient_id INTEGER,
  doctor_id INTEGER,
  appoint_time TEXT,
  status TEXT,
  fee REAL
);
CREATE TABLE prescriptions (
  prescription_id INTEGER PRIMARY KEY,
  appointment_id INTEGER,
  medicine_name TEXT,
  dosage TEXT,
  quantity INTEGER,
  price REAL
);
CREATE TABLE medicines (
  medicine_id INTEGER PRIMARY KEY,
  medicine_name TEXT NOT NULL,
  category TEXT,
  stock INTEGER,
  unit_price REAL,
  expiry_date TEXT
);
