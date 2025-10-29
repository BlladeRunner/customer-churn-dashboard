import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

plt.rcParams["figure.figsize"] = (9,5)
OUT = Path("outputs"); OUT.mkdir(exist_ok=True)
con = sqlite3.connect("db/churn.db")

# KPI
kpi = pd.read_sql("SELECT * FROM v_kpi;", con)
print(kpi)

# 1) Contract type
df = pd.read_sql("SELECT * FROM v_churn_by_contract;", con).sort_values("churn_rate_pct", ascending=False)
ax = sns.barplot(data=df, x="contract_type", y="churn_rate_pct")
ax.set_title("Churn rate by Contract Type (%)"); ax.set_xlabel(""); ax.set_ylabel("%")
plt.tight_layout(); plt.savefig(OUT/"churn_by_contract.png"); plt.close()

# 2) Tenure buckets
df = pd.read_sql("SELECT * FROM v_churn_by_tenure;", con)
order = ["0-6m","6-12m","12-24m","24-36m","36m+"]
df["tenure_bucket"] = pd.Categorical(df["tenure_bucket"], order)
df = df.sort_values("tenure_bucket")
ax = sns.lineplot(data=df, x="tenure_bucket", y="churn_rate_pct", marker="o")
ax.set_title("Churn vs Tenure (%)"); ax.set_xlabel("Tenure bucket"); ax.set_ylabel("%")
plt.tight_layout(); plt.savefig(OUT/"churn_by_tenure.png"); plt.close()

# 3) Internet service
df = pd.read_sql("SELECT * FROM v_churn_by_internet;", con).sort_values("churn_rate_pct", ascending=False)
ax = sns.barplot(data=df, x="internet", y="churn_rate_pct")
ax.set_title("Churn by Internet Service (%)"); ax.set_xlabel(""); ax.set_ylabel("%")
plt.tight_layout(); plt.savefig(OUT/"churn_by_internet.png"); plt.close()

# 4) Monthly charges bands
sql = """
SELECT
  CASE
    WHEN MonthlyCharges < 40 THEN '<$40'
    WHEN MonthlyCharges < 70 THEN '$40–70'
    ELSE '>$70'
  END AS band,
  ROUND(AVG(churn)*100.0,2) AS churn_rate_pct
FROM customers
GROUP BY band
ORDER BY churn_rate_pct DESC;
"""
df = pd.read_sql(sql, con)
ax = sns.barplot(data=df, x="band", y="churn_rate_pct")
ax.set_title("Churn vs Monthly Charges (%)"); ax.set_xlabel("Monthly charge band"); ax.set_ylabel("%")
plt.tight_layout(); plt.savefig(OUT/"churn_by_charge_band.png"); plt.close()

print("PNG graphs are saved in outputs/")
