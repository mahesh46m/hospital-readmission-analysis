-- Readmission & utilization analysis.
-- A readmission is a later admission for the same patient starting within
-- 30 days of the previous discharge.

WITH ordered AS (
    SELECT
        a.*,
        LEAD(admit_date) OVER (PARTITION BY patient_id ORDER BY admit_date) AS next_admit
    FROM admissions a
),
flagged AS (
    SELECT
        *,
        CASE WHEN next_admit IS NOT NULL
                  AND julianday(next_admit) - julianday(discharge_date) <= 30
             THEN 1 ELSE 0 END AS readmit_30d
    FROM ordered
)
SELECT * FROM flagged;

-- Sections below are run individually by run_analysis.py:
-- :overall      SELECT AVG(readmit_30d), COUNT(*) FROM flagged
-- :by_diagnosis SELECT diagnosis, COUNT(*), AVG(readmit_30d), AVG(julianday(discharge_date)-julianday(admit_date)) FROM flagged GROUP BY 1
-- :by_age       SELECT age_band, COUNT(*), AVG(readmit_30d) FROM flagged GROUP BY 1
-- :by_dept      SELECT department, COUNT(*), AVG(readmit_30d), AVG(julianday(discharge_date)-julianday(admit_date)) FROM flagged GROUP BY 1
-- :monthly      SELECT substr(admit_date,1,7), COUNT(*) FROM admissions GROUP BY 1
-- :dispo        SELECT discharge_dispo, COUNT(*), AVG(readmit_30d) FROM flagged GROUP BY 1
