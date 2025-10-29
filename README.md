# 📊 Customer Churn Dashboard (SQL + Python)

## 📘 Project Overview

This project analyzes customer churn patterns in a telecom company using **SQL (SQLite)** and **Python (pandas)**.  
The goal is to identify retention trends, churn drivers, and customer behavior based on demographic and service usage data.

---

## 🧱 Database Schema

**Table:** `customers` (7,043 rows)

| Column            | Type    | Description                          |
| ----------------- | ------- | ------------------------------------ |
| customerID        | TEXT    | Unique customer identifier           |
| gender            | TEXT    | Male / Female                        |
| senior_citizen    | INTEGER | 1 = Yes, 0 = No                      |
| partner           | INTEGER | 1 = Has partner                      |
| dependents        | INTEGER | 1 = Has dependents                   |
| tenure            | INTEGER | Months as a customer                 |
| phone_service     | INTEGER | 1 = Active phone service             |
| multiple_lines    | TEXT    | Yes/No/No phone service              |
| internet_service  | TEXT    | DSL / Fiber optic / None             |
| online_security   | TEXT    | Yes/No/No internet service           |
| online_backup     | TEXT    | Yes/No/No internet service           |
| device_protection | TEXT    | Yes/No/No internet service           |
| tech_support      | TEXT    | Yes/No/No internet service           |
| streaming_tv      | TEXT    | Yes/No/No internet service           |
| streaming_movies  | TEXT    | Yes/No/No internet service           |
| contract          | TEXT    | Month-to-month / One year / Two year |
| paperless_billing | INTEGER | 1 = Yes                              |
| payment_method    | TEXT    | Payment method                       |
| monthly_charges   | REAL    | Monthly payment                      |
| total_charges     | REAL    | Total paid amount                    |
| churn             | INTEGER | 1 = Customer left, 0 = Active        |

---

## ⚙️ Tools & Technologies

- **Python 3.12+** → Data preprocessing (pandas, sqlite3)
- **SQLite 3.50+** → Database management and SQL analysis
- **VS Code + SQLTools** → Interactive SQL queries
- _(Optional)_ Power BI or Tableau → Dashboard visualization

---

## 🧮 SQL Highlights

- Customer churn distribution by demographics and contract type
- Monthly revenue and churn segmentation
- Average tenure and billing behavior by churn status
- Correlation between internet service and churn
- Churn by payment method and contract type

Example:

```sql
SELECT
  contract,
  ROUND(AVG(monthly_charges), 2) AS avg_monthly,
  ROUND(SUM(churn)*100.0/COUNT(*), 2) AS churn_rate
FROM customers
GROUP BY contract
ORDER BY churn_rate DESC;
```

📊 Key Insights

Short-term contracts (month-to-month) show the highest churn rate.
Paperless billing and electronic payments correlate with higher churn — likely due to low commitment.
Senior citizens and fiber-optic internet users tend to churn more often.
Customers with online security and tech support are less likely to churn.
Longer tenure (>24 months) strongly correlates with customer retention.
