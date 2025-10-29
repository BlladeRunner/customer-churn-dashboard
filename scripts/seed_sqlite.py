import sqlite3, pandas as pd
from pathlib import Path

# ----- paths
ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "data" / "raw"
DB_PATH = ROOT / "db" / "churn.db"

candidates = sorted(CSV_DIR.glob("*.csv"))
if not candidates:
    raise FileNotFoundError(f"CSV не найден в {CSV_DIR}")
csv_path = candidates[0]

df = pd.read_csv(csv_path)

# ----- normalize column names
df.columns = (
    df.columns.str.strip()
              .str.lower()
              .str.replace(' ', '_', regex=False)
              .str.replace('-', '_', regex=False)
              .str.replace(r'[^\w_]', '', regex=True)
)

def pick(col_main, *alts):
    for name in (col_main, *alts):
        if name in df.columns:
            return name
    raise KeyError(f"Не найдена колонка '{col_main}' (альт.: {alts}). "
                   f"В CSV есть: {list(df.columns)}")

# ----- align the key fields to our scheme
col_customer_id     = pick("customerid", "customer_id", "customer_id_")
col_gender          = pick("gender")
col_senior_citizen  = pick("senior_citizen", "seniorcitizen")
col_partner         = pick("partner")
col_dependents      = pick("dependents")
col_tenure          = pick("tenure")
col_phone_service   = pick("phone_service", "phoneservice")
col_multiple_lines  = pick("multiple_lines", "multiplelines")
col_internet_service= pick("internet_service", "internetservice")
col_online_security = pick("online_security", "onlinesecurity")
col_online_backup   = pick("online_backup", "onlinebackup")
col_device_protect  = pick("device_protection", "deviceprotection")
col_tech_support    = pick("tech_support", "techsupport")
col_stream_tv       = pick("streaming_tv", "streamingtv")
col_stream_movies   = pick("streaming_movies", "streamingmovies")
col_contract        = pick("contract")
col_paperless       = pick("paperless_billing", "paperlessbilling")
col_payment_method  = pick("payment_method", "paymentmethod")
col_monthly         = pick("monthly_charges", "monthlycharges")
col_total           = pick("total_charges", "totalcharges", "total_charges_")
col_churn           = pick("churn")

# ----- collecting the final DataFrame with our names
out = pd.DataFrame({
    "customerID":        df[col_customer_id],
    "gender":            df[col_gender],
    "senior_citizen":    df[col_senior_citizen],
    "partner":           df[col_partner],
    "dependents":        df[col_dependents],
    "tenure":            df[col_tenure],
    "phone_service":     df[col_phone_service],
    "multiple_lines":    df[col_multiple_lines],
    "internet_service":  df[col_internet_service],
    "online_security":   df[col_online_security],
    "online_backup":     df[col_online_backup],
    "device_protection": df[col_device_protect],
    "tech_support":      df[col_tech_support],
    "streaming_tv":      df[col_stream_tv],
    "streaming_movies":  df[col_stream_movies],
    "contract":          df[col_contract],
    "paperless_billing": df[col_paperless],
    "payment_method":    df[col_payment_method],
    "monthly_charges":   df[col_monthly],
    "total_charges":     df[col_total],
    "churn":             df[col_churn],
})

# ----- typing / cleaning
for c in ["monthly_charges", "total_charges", "tenure"]:
    out[c] = pd.to_numeric(out[c], errors="coerce")

# binary Yes/No → 1/0
def yn_to01(s):
    return s.map({"Yes": 1, "No": 0}).fillna(s)

for c in ["partner","dependents","phone_service","paperless_billing","churn"]:
    out[c] = yn_to01(out[c]).astype("Int64")

# senior_citizen is already 0/1 for most datasets; let's bring it to Int64
out["senior_citizen"] = pd.to_numeric(out["senior_citizen"], errors="coerce").astype("Int64")

# ----- creating a database
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
conn = sqlite3.connect(DB_PATH)
cur  = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customerID         TEXT PRIMARY KEY,
    gender             TEXT,
    senior_citizen     INTEGER,
    partner            INTEGER,
    dependents         INTEGER,
    tenure             INTEGER,
    phone_service      INTEGER,
    multiple_lines     TEXT,
    internet_service   TEXT,
    online_security    TEXT,
    online_backup      TEXT,
    device_protection  TEXT,
    tech_support       TEXT,
    streaming_tv       TEXT,
    streaming_movies   TEXT,
    contract           TEXT,
    paperless_billing  INTEGER,
    payment_method     TEXT,
    monthly_charges    REAL,
    total_charges      REAL,
    churn              INTEGER
);
""")

out.to_sql("customers", conn, if_exists="append", index=False)
conn.commit()
conn.close()

print(f"OK: loaded {len(out):,} lines in {DB_PATH}")
