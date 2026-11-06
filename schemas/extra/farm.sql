CREATE TABLE field_plot (id INTEGER PRIMARY KEY, plot_name TEXT, area_hectare REAL, soil_type TEXT);
CREATE TABLE crop (id INTEGER PRIMARY KEY, crop_name TEXT, variety TEXT, planted_at TEXT, expected_harvest TEXT);
CREATE TABLE planting (id INTEGER PRIMARY KEY, field_plot_id INTEGER, crop_id INTEGER, planted_at TEXT, seed_cost REAL, status TEXT);
CREATE TABLE harvest (id INTEGER PRIMARY KEY, planting_id INTEGER, harvest_date TEXT, yield_kg REAL, sale_price_per_kg REAL);
