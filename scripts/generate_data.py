"""Generate a deterministic synthetic hospital admissions dataset.

All data is randomly generated with a fixed seed. It is not patient data,
does not come from any hospital or employer, and the numbers are not
real-world metrics.

Model: each patient gets 1-4 index episodes spaced well over 30 days apart.
An index episode may spawn at most one readmission, starting within 30 days
of discharge, with probability driven by diagnosis group and age band.
"""
import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

SEED = 13
N_PATIENTS = 1100
ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "hospital.db"

# diagnosis group: (weight, mean_los, base_30d_readmit_prob)
DIAGNOSES = [
    ("CHF", 0.16, 5.5, 0.21),
    ("Pneumonia", 0.15, 4.5, 0.15),
    ("AMI", 0.10, 4.0, 0.12),
    ("COPD", 0.14, 4.2, 0.19),
    ("Diabetes", 0.12, 3.6, 0.13),
    ("Renal failure", 0.10, 5.0, 0.22),
    ("Orthopedic", 0.12, 3.2, 0.06),
    ("GI", 0.11, 3.4, 0.11),
]
AGE_BANDS = [("18-44", 0.22), ("45-64", 0.33), ("65-74", 0.24), ("75+", 0.21)]
DEPARTMENTS = [("Cardiology", 0.28), ("Internal Medicine", 0.34),
               ("Pulmonology", 0.18), ("Orthopedics", 0.12), ("Gastroenterology", 0.08)]
DISPO = [("home", 0.62), ("home_health", 0.18), ("snf", 0.14), ("rehab", 0.06)]
AGE_RISK = {"18-44": -0.05, "45-64": 0.0, "65-74": 0.03, "75+": 0.06}
EPISODES = [(1, 0.45), (2, 0.30), (3, 0.15), (4, 0.10)]
LAST_DAY = 364  # keep everything inside 2025


def pick(rng, table):
    # Each row is (value, weight, ...); only the first two are used.
    r = rng.random()
    acc = 0.0
    for row in table:
        acc += row[1]
        if r <= acc:
            return row[0]
    return table[-1][0]


def main() -> None:
    rng = random.Random(SEED)
    con = sqlite3.connect(DB)
    con.executescript((ROOT / "sql" / "schema.sql").read_text())
    con.execute("DELETE FROM admissions")

    base = date(2025, 1, 1)
    aid = 0
    for p in range(1, N_PATIENTS + 1):
        patient = f"PT{p:04d}"
        age = pick(rng, AGE_BANDS)
        day = rng.randint(0, 240)
        for _ in range(pick(rng, EPISODES)):
            diag = pick(rng, DIAGNOSES)
            mean_los = {d[0]: d[2] for d in DIAGNOSES}[diag]
            los = max(1, int(rng.gauss(mean_los, 1.8)))
            admit_day = day
            if admit_day + los > LAST_DAY:
                break
            dispo = pick(rng, DISPO)
            dept = pick(rng, DEPARTMENTS)
            aid += 1
            con.execute(
                "INSERT INTO admissions VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (f"A{aid:05d}", patient, str(base + timedelta(days=admit_day)),
                 str(base + timedelta(days=admit_day + los)),
                 diag, age, dept, dispo),
            )
            # At most one readmission, within 30 days of this discharge.
            p_readmit = {d[0]: d[3] for d in DIAGNOSES}[diag] + AGE_RISK[age]
            if rng.random() < p_readmit:
                r_day = admit_day + los + rng.randint(1, 25)
                r_los = max(1, int(rng.gauss(mean_los, 1.8)))
                if r_day + r_los <= LAST_DAY:
                    aid += 1
                    con.execute(
                        "INSERT INTO admissions VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (f"A{aid:05d}", patient, str(base + timedelta(days=r_day)),
                         str(base + timedelta(days=r_day + r_los)),
                         diag, age, pick(rng, DEPARTMENTS), pick(rng, DISPO)),
                    )
            day += rng.randint(45, 120)  # next index episode stays >30d clear
            if day > LAST_DAY - 10:
                break

    con.commit()
    (n,) = con.execute("SELECT COUNT(*) FROM admissions").fetchone()
    con.close()
    print(f"wrote {DB}: {n} admissions for {N_PATIENTS} patients")


if __name__ == "__main__":
    main()
