-- Schema for the hospital readmission & utilization demo (SQLite dialect).

CREATE TABLE admissions (
    admission_id   TEXT PRIMARY KEY,
    patient_id     TEXT NOT NULL,
    admit_date     TEXT NOT NULL,     -- ISO yyyy-mm-dd
    discharge_date TEXT NOT NULL,
    diagnosis      TEXT NOT NULL,     -- diagnosis group, e.g. "CHF"
    age_band       TEXT NOT NULL,     -- 18-44, 45-64, 65-74, 75+
    department     TEXT NOT NULL,
    discharge_dispo TEXT NOT NULL     -- home, home_health, snf, rehab
);
