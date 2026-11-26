# Hospital readmission & utilization summary (synthetic data)

Produced by `scripts/run_analysis.py`. A readmission is a later admission
for the same patient starting within 30 days of the previous discharge.

## Headline KPIs

| KPI | Value |
|---|---|
| Admissions | 2,283 |
| Unique patients | 1,100 |
| 30-day readmission rate | **14.8%** |
| Readmissions within 30d | 337 |
| Average length of stay | 3.8 days |

## 30-day readmission rate by diagnosis group

| Diagnosis | Admissions | Readmit rate | Avg LOS |
|---|---|---|---|
| CHF | 407 | 19.4% | 5.0 |
| COPD | 332 | 18.4% | 3.7 |
| Renal failure | 204 | 17.6% | 4.6 |
| Pneumonia | 316 | 15.5% | 4.1 |
| Diabetes | 262 | 15.3% | 3.2 |
| GI | 276 | 11.2% | 3.2 |
| AMI | 209 | 11.0% | 3.5 |
| Orthopedic | 277 | 6.5% | 2.9 |

## 30-day readmission rate by age band

| Age band | Admissions | Readmit rate |
|---|---|---|
| 18-44 | 486 | 10.5% |
| 45-64 | 772 | 14.5% |
| 65-74 | 554 | 17.3% |
| 75+ | 471 | 16.6% |

## Utilization by department

| Department | Admissions | Readmit rate | Avg LOS |
|---|---|---|---|
| Internal Medicine | 805 | 14.8% | 3.7 |
| Cardiology | 642 | 14.3% | 3.8 |
| Pulmonology | 409 | 17.6% | 3.8 |
| Orthopedics | 267 | 12.0% | 4.1 |
| Gastroenterology | 160 | 13.8% | 3.9 |

## Readmission by discharge disposition

| Disposition | Admissions | Readmit rate |
|---|---|---|
| home | 1397 | 15.0% |
| home_health | 420 | 14.8% |
| snf | 327 | 14.4% |
| rehab | 139 | 13.7% |

## Monthly admissions (utilization trend)

| Month | Admissions |
|---|---|
| 2025-01 | 145 |
| 2025-02 | 136 |
| 2025-03 | 190 |
| 2025-04 | 227 |
| 2025-05 | 260 |
| 2025-06 | 272 |
| 2025-07 | 299 |
| 2025-08 | 282 |
| 2025-09 | 168 |
| 2025-10 | 137 |
| 2025-11 | 116 |
| 2025-12 | 51 |
