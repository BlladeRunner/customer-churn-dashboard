-- General KPIs
SELECT * FROM v_kpi;

-- Outflow by type of contract
SELECT * FROM v_churn_by_contract ORDER BY churn_rate_pct DESC;

-- Outflow by length of service (tenure buckets)
SELECT * FROM v_churn_by_tenure ORDER BY churn_rate_pct DESC;

-- Outflow by type of Internet
SELECT * FROM v_churn_by_internet ORDER BY churn_rate_pct DESC;

-- Top factors (rough cut: payments vs churn)
SELECT
  CASE
    WHEN MonthlyCharges < 40 THEN '<$40'
    WHEN MonthlyCharges < 70 THEN '$40–70'
    ELSE '>$70'
  END AS charge_band,
  COUNT(*) AS customers,
  ROUND(AVG(churn)*100.0,2) AS churn_rate_pct
FROM customers
GROUP BY charge_band
ORDER BY churn_rate_pct DESC;
