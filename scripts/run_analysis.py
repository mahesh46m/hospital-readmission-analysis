"""Run the readmission & utilization analysis and write sample_output.md
(a Power BI-style KPI summary in markdown).

Runs generate_data.py first if the database is missing.
"""
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "hospital.db"

FLAGGED = """
WITH ordered AS (
    SELECT a.*, LEAD(admit_date) OVER (PARTITION BY patient_id ORDER BY admit_date) AS next_admit
    FROM admissions a
),
flagged AS (
    SELECT *,
        CASE WHEN next_admit IS NOT NULL
                  AND julianday(next_admit) - julianday(discharge_date) <= 30
             THEN 1 ELSE 0 END AS readmit_30d
    FROM ordered
)
"""


def pct(x) -> str:
    return f"{100 * x:.1f}%"


def main() -> None:
    if not DB.exists():
        import generate_data  # noqa: PLC0415 - sibling script

        generate_data.main()
    con = sqlite3.connect(DB)

    (n_adm, n_patients) = con.execute(
        "SELECT COUNT(*), COUNT(DISTINCT patient_id) FROM admissions").fetchone()
    (readmit_rate,) = con.execute(
        FLAGGED + "SELECT AVG(readmit_30d) FROM flagged").fetchone()
    (avg_los,) = con.execute(
        "SELECT AVG(julianday(discharge_date) - julianday(admit_date)) FROM admissions"
    ).fetchone()
    n_readmits = con.execute(
        FLAGGED + "SELECT SUM(readmit_30d) FROM flagged").fetchone()[0]

    by_diag = con.execute(
        FLAGGED + """
        SELECT diagnosis, COUNT(*), AVG(readmit_30d),
               AVG(julianday(discharge_date) - julianday(admit_date))
        FROM flagged GROUP BY 1 ORDER BY 3 DESC""").fetchall()
    by_age = con.execute(
        FLAGGED + """
        SELECT age_band, COUNT(*), AVG(readmit_30d)
        FROM flagged GROUP BY 1
        ORDER BY CASE age_band WHEN '18-44' THEN 1 WHEN '45-64' THEN 2
                               WHEN '65-74' THEN 3 ELSE 4 END""").fetchall()
    by_dept = con.execute(
        FLAGGED + """
        SELECT department, COUNT(*), AVG(readmit_30d),
               AVG(julianday(discharge_date) - julianday(admit_date))
        FROM flagged GROUP BY 1 ORDER BY 2 DESC""").fetchall()
    by_dispo = con.execute(
        FLAGGED + """
        SELECT discharge_dispo, COUNT(*), AVG(readmit_30d)
        FROM flagged GROUP BY 1 ORDER BY 2 DESC""").fetchall()
    monthly = con.execute(
        "SELECT substr(admit_date, 1, 7), COUNT(*) FROM admissions GROUP BY 1"
    ).fetchall()
    con.close()

    out = [
        "# Hospital readmission & utilization summary (synthetic data)",
        "",
        "Produced by `scripts/run_analysis.py`. A readmission is a later admission",
        "for the same patient starting within 30 days of the previous discharge.",
        "",
        "## Headline KPIs",
        "",
        "| KPI | Value |",
        "|---|---|",
        f"| Admissions | {n_adm:,} |",
        f"| Unique patients | {n_patients:,} |",
        f"| 30-day readmission rate | **{pct(readmit_rate)}** |",
        f"| Readmissions within 30d | {n_readmits} |",
        f"| Average length of stay | {avg_los:.1f} days |",
        "",
        "## 30-day readmission rate by diagnosis group",
        "",
        "| Diagnosis | Admissions | Readmit rate | Avg LOS |",
        "|---|---|---|---|",
        *[f"| {d} | {c} | {pct(r)} | {los:.1f} |" for d, c, r, los in by_diag],
        "",
        "## 30-day readmission rate by age band",
        "",
        "| Age band | Admissions | Readmit rate |",
        "|---|---|---|",
        *[f"| {a} | {c} | {pct(r)} |" for a, c, r in by_age],
        "",
        "## Utilization by department",
        "",
        "| Department | Admissions | Readmit rate | Avg LOS |",
        "|---|---|---|---|",
        *[f"| {d} | {c} | {pct(r)} | {los:.1f} |" for d, c, r, los in by_dept],
        "",
        "## Readmission by discharge disposition",
        "",
        "| Disposition | Admissions | Readmit rate |",
        "|---|---|---|",
        *[f"| {d} | {c} | {pct(r)} |" for d, c, r in by_dispo],
        "",
        "## Monthly admissions (utilization trend)",
        "",
        "| Month | Admissions |",
        "|---|---|",
        *[f"| {m} | {c} |" for m, c in monthly],
        "",
    ]
    (ROOT / "sample_output.md").write_text("\n".join(out) + "\n")
    print("\n".join(out[:26]))


if __name__ == "__main__":
    main()
