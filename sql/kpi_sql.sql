-- Clients with the highest probability of churn (simple heuristic: >$70 and 0-6m experience)
SELECT customerID, tenure, tenure_bucket, MonthlyCharges, Contract, InternetService, churn
FROM customers
WHERE MonthlyCharges >= 70 AND tenure <= 6
ORDER BY MonthlyCharges DESC
LIMIT 25;
