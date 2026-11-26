# Hospital Readmission & Utilization Analysis

A portfolio project by **Mahesh M**: 30-day readmission and utilization analysis over a synthetic hospital admissions dataset, in SQL + Python, written up as a Power BI-style KPI summary.

> **Demo project.** All data is synthetic and randomly generated (fixed seed). It is not patient data, does not come from any hospital or employer, and the numbers are not real-world metrics.

## What it does

1. **Generate** (`scripts/generate_data.py`): 1,100 synthetic patients with 1-4 index admission episodes each, spaced well over 30 days apart. Each episode may spawn at most one readmission within 30 days of discharge, with probability driven by diagnosis group (CHF 21%, renal failure 22%, orthopedic 6%, ...) and age band.
2. **Analyze** (`sql/analysis.sql` + `scripts/run_analysis.py`): a readmission is a later admission for the same patient starting within 30 days of the previous discharge (window function over per-patient admissions). Computes the headline KPIs, readmission rates by diagnosis group, age band and discharge disposition, utilization by department and monthly admission trend.

## Headline results (seed 13)

| KPI | Value |
|---|---|
| Admissions | 2,283 |
| Unique patients | 1,100 |
| 30-day readmission rate | 14.8% |
| Average length of stay | 3.9 days |

Highest readmission rates: CHF 19.4%, COPD 18.4%, renal failure 17.6%; lowest: orthopedic 6.5%. Full tables in [`sample_output.md`](sample_output.md).

## Run it

Requires Python 3.8+ only (built-in `sqlite3`, no installs).

```bash
python scripts/run_analysis.py   # builds hospital.db on first run
```

## Layout

```
sql/schema.sql            admissions table
sql/analysis.sql          the readmission CTE + section queries
scripts/generate_data.py  deterministic synthetic admissions
scripts/run_analysis.py   computes KPIs, writes sample_output.md
```

## Possible extensions

Risk-adjusted rates (comorbidity scores), LACE index stratification, excess-day analysis, and a Power BI dashboard over the same query layer.

---
Author: Mahesh M. Released under the MIT License.
