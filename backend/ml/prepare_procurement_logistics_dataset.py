"""Prepare a unified procurement + logistics dataset for Module A and Module B.

This script cleans raw procurement and logistics inputs, engineers the delay label and
price anomaly score, connects both datasets via a supplier reliability bucket, and
writes processed outputs to backend/data/processed.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"

PROCUREMENT_PATH = RAW_DIR / "procurement_raw.csv"
LOGISTICS_PATH = RAW_DIR / "logistics_raw.csv"
CLEANED_PROCUREMENT_PATH = PROCESSED_DIR / "procurement_cleaned.csv"
CLEANED_LOGISTICS_PATH = PROCESSED_DIR / "logistics_cleaned.csv"
UNIFIED_PATH = PROCESSED_DIR / "unified_procurement_logistics.csv"
SYNTHETIC_PROCUREMENT_PATH = PROCESSED_DIR / "procurement_synthetic_expanded.csv"

SUPPLIER_RELIABILITY_MAP = {
    "Alpha_Inc": 0.92,
    "Beta_Supplies": 0.83,
    "Gamma_Co": 0.76,
    "Delta_Logistics": 0.68,
    "Epsilon_Group": 0.55,
}

SUPPLIER_BUCKETS = [0.0, 0.6, 0.7, 0.8, 0.9, 1.0]
SUPPLIER_BUCKET_LABELS = [
    "very_low",
    "low",
    "medium",
    "high",
    "very_high",
]

ITEM_LEAD_TIME_DAYS = {
    "Office Supplies": 7,
    "MRO": 10,
    "Packaging": 8,
    "Raw Materials": 12,
    "Electronics": 9,
}

ORDER_STATUS_GROUP = {
    "Delivered": "delivered",
    "Pending": "pending",
    "Cancelled": "cancelled",
    "Partially Delivered": "partial",
}


def ensure_processed_dir() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def clean_procurement(procurement: pd.DataFrame) -> pd.DataFrame:
    df = procurement.copy()
    df.columns = df.columns.str.strip()

    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    df["Delivery_Date"] = pd.to_datetime(df["Delivery_Date"], errors="coerce")

    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0).astype(int)
    df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce")
    df["Negotiated_Price"] = pd.to_numeric(df["Negotiated_Price"], errors="coerce")
    df["Defective_Units"] = pd.to_numeric(df["Defective_Units"], errors="coerce").fillna(0).astype(int)

    df["Unit_Price"] = df["Unit_Price"].fillna(df["Negotiated_Price"]).fillna(0.0)
    df["Negotiated_Price"] = df["Negotiated_Price"].fillna(df["Unit_Price"])

    df["Compliance"] = df["Compliance"].astype(str).str.strip().str.lower()
    df["Compliance_Flag"] = (df["Compliance"] == "yes").astype(int)

    df["Order_Status"] = df["Order_Status"].astype(str).str.strip()
    df["Order_Status_Clean"] = df["Order_Status"].replace(ORDER_STATUS_GROUP)

    df["Expected_Delivery_Days"] = df["Item_Category"].map(ITEM_LEAD_TIME_DAYS).fillna(10).astype(int)
    df["Expected_Delivery_Date"] = df["Order_Date"] + pd.to_timedelta(df["Expected_Delivery_Days"], unit="D")

    estimated_delivery = df["Order_Date"] + pd.to_timedelta(df["Expected_Delivery_Days"], unit="D")
    df["Delivery_Date"] = df["Delivery_Date"].fillna(estimated_delivery)

    df["Delivery_Delay_Days"] = (df["Delivery_Date"] - df["Expected_Delivery_Date"]).dt.days.fillna(0).astype(int)
    df["Delivery_Delay_Days"] = df["Delivery_Delay_Days"].clip(lower=0)

    df["Delay_Label"] = (
        df["Order_Status"].isin(["Pending", "Cancelled", "Partially Delivered"]) |
        (df["Delivery_Delay_Days"] > 0)
    ).astype(int)

    df["Defective_Rate"] = np.where(df["Quantity"] > 0, df["Defective_Units"] / df["Quantity"], 0.0)
    df["Price_Gap"] = df["Unit_Price"] - df["Negotiated_Price"]
    df["Price_Gap_Pct"] = np.where(df["Unit_Price"] > 0, df["Price_Gap"] / df["Unit_Price"], 0.0)

    price_gap_pct = df["Price_Gap_Pct"].abs().replace(np.inf, np.nan).fillna(0.0)
    df["Price_Anomaly_Score"] = (price_gap_pct - price_gap_pct.min()) / (price_gap_pct.max() - price_gap_pct.min() + 1e-9)

    df["Supplier_Reliability_Score"] = df["Supplier"].map(SUPPLIER_RELIABILITY_MAP).fillna(0.65)
    df["Supplier_Reliability_Bucket"] = pd.cut(
        df["Supplier_Reliability_Score"], bins=SUPPLIER_BUCKETS, labels=SUPPLIER_BUCKET_LABELS, include_lowest=True
    )

    df = df.drop(columns=["Compliance"])
    df = df[[
        "PO_ID",
        "Supplier",
        "Supplier_Reliability_Score",
        "Supplier_Reliability_Bucket",
        "Order_Date",
        "Delivery_Date",
        "Expected_Delivery_Date",
        "Expected_Delivery_Days",
        "Order_Status",
        "Order_Status_Clean",
        "Item_Category",
        "Quantity",
        "Unit_Price",
        "Negotiated_Price",
        "Defective_Units",
        "Compliance_Flag",
        "Defective_Rate",
        "Delivery_Delay_Days",
        "Delay_Label",
        "Price_Gap",
        "Price_Gap_Pct",
        "Price_Anomaly_Score",
    ]]

    return df


def clean_logistics(logistics: pd.DataFrame) -> pd.DataFrame:
    df = logistics.copy()
    df.columns = df.columns.str.strip()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df[df["timestamp"].notna()].reset_index(drop=True)

    df["supplier_reliability_score"] = pd.to_numeric(df["supplier_reliability_score"], errors="coerce").fillna(0.0)
    df["delay_probability"] = pd.to_numeric(df["delay_probability"], errors="coerce").fillna(0.0)
    df["delivery_time_deviation"] = pd.to_numeric(df["delivery_time_deviation"], errors="coerce").fillna(0.0)
    df["eta_variation_hours"] = pd.to_numeric(df["eta_variation_hours"], errors="coerce").fillna(0.0)
    df["traffic_congestion_level"] = pd.to_numeric(df["traffic_congestion_level"], errors="coerce").fillna(0.0)
    df["weather_condition_severity"] = pd.to_numeric(df["weather_condition_severity"], errors="coerce").fillna(0.0)
    df["port_congestion_level"] = pd.to_numeric(df["port_congestion_level"], errors="coerce").fillna(0.0)
    df["shipping_costs"] = pd.to_numeric(df["shipping_costs"], errors="coerce").fillna(df["shipping_costs"].median())
    df["warehouse_inventory_level"] = pd.to_numeric(df["warehouse_inventory_level"], errors="coerce").fillna(df["warehouse_inventory_level"].median())

    df["supplier_reliability_bucket"] = pd.cut(
        df["supplier_reliability_score"], bins=SUPPLIER_BUCKETS, labels=SUPPLIER_BUCKET_LABELS, include_lowest=True
    )
    df["logistic_date"] = df["timestamp"].dt.normalize()
    return df


def aggregate_logistics(logistics: pd.DataFrame) -> pd.DataFrame:
    feature_columns = [
        "eta_variation_hours",
        "traffic_congestion_level",
        "warehouse_inventory_level",
        "weather_condition_severity",
        "port_congestion_level",
        "shipping_costs",
        "delay_probability",
        "delivery_time_deviation",
    ]
    grouped = (
        logistics
        .groupby("supplier_reliability_bucket", observed=True)[feature_columns]
        .median()
        .rename(columns={col: f"logistics_median_{col}" for col in feature_columns})
        .reset_index()
    )
    return grouped


def merge_procurement_and_logistics(
    procurement: pd.DataFrame,
    logistics_agg: pd.DataFrame,
) -> pd.DataFrame:
    merged = procurement.merge(
        logistics_agg,
        how="left",
        left_on="Supplier_Reliability_Bucket",
        right_on="supplier_reliability_bucket",
    )

    merged = merged.sort_values(["Supplier", "Order_Date"]).reset_index(drop=True)

    merged["vendor_id"] = merged["Supplier"].astype("category").cat.codes + 1
    merged["material_group"] = merged["Item_Category"].replace(
        {
            "Office Supplies": "office",
            "MRO": "operations",
            "Packaging": "packaging",
            "Raw Materials": "raw_materials",
            "Electronics": "electronics",
        }
    )
    merged["item_category"] = merged["Item_Category"]

    merged["supplier_reliability_score"] = merged["Supplier_Reliability_Score"]
    merged["price_anomaly_score"] = merged["Price_Anomaly_Score"]
    merged["delay_probability"] = merged["logistics_median_delay_probability"].fillna(0.0)
    merged["delivery_time_deviation"] = merged["logistics_median_delivery_time_deviation"].fillna(0.0)

    merged["rolling_delay_rate"] = (
        merged.groupby("Supplier")["Delay_Label"].transform(lambda s: s.rolling(5, min_periods=1).mean())
    )
    merged["price_volatility_index"] = (
        merged.groupby("Supplier")["Price_Gap_Pct"].transform(lambda s: s.rolling(5, min_periods=1).std().fillna(0.0))
    )

    merged = merged.drop(columns=["supplier_reliability_bucket"])
    return merged


def synthesize_procurement_records(procurement: pd.DataFrame, target_size: int = 5000) -> pd.DataFrame:
    if len(procurement) >= target_size:
        return procurement.copy()

    synth_rows: list[dict] = []
    rng = np.random.default_rng(42)
    suppliers = procurement["Supplier"].unique().tolist()
    categories = procurement["Item_Category"].unique().tolist()
    statuses = ["Delivered", "Pending", "Cancelled", "Partially Delivered"]
    supplier_scores = procurement.set_index("Supplier")["Supplier_Reliability_Score"].to_dict()

    current_max = int(procurement["PO_ID"].str.extract(r"(\d+)")[0].astype(int).max())

    for idx in range(target_size - len(procurement)):
        source = procurement.sample(random_state=rng.integers(0, 1_000_000)).iloc[0]
        supplier = rng.choice(suppliers)
        item_category = rng.choice(categories)
        order_date = source["Order_Date"] + pd.to_timedelta(rng.integers(-30, 31), unit="D")
        expected_days = ITEM_LEAD_TIME_DAYS.get(item_category, 10)
        expected_delivery = order_date + pd.to_timedelta(expected_days, unit="D")
        delay = int(rng.choice([0, 0, 0, 1, 2, 3, 5, 7]))
        delivery_date = expected_delivery + pd.to_timedelta(delay, unit="D")
        status = rng.choice(statuses, p=[0.7, 0.15, 0.05, 0.1])
        quantity = max(1, int(source["Quantity"] * float(rng.normal(1.0, 0.15))))
        unit_price = max(0.1, float(source["Unit_Price"] * float(rng.normal(1.0, 0.12))))
        negotiated_price = max(0.0, float(unit_price * float(rng.normal(0.95, 0.07))))
        defective_units = min(quantity, int(abs(rng.poisson(0.03 * quantity))))
        compliance_flag = int(rng.choice([1, 1, 1, 0], p=[0.7, 0.1, 0.1, 0.1]))

        synth_rows.append(
            {
                "PO_ID": f"PO-{current_max + idx + 1:05d}",
                "Supplier": supplier,
                "Order_Date": order_date,
                "Delivery_Date": delivery_date,
                "Item_Category": item_category,
                "Order_Status": status,
                "Quantity": quantity,
                "Unit_Price": unit_price,
                "Negotiated_Price": negotiated_price,
                "Defective_Units": defective_units,
                "Compliance_Flag": compliance_flag,
                "Supplier_Reliability_Score": supplier_scores.get(supplier, 0.65),
            }
        )

    synth_df = pd.DataFrame(synth_rows)
    synth_df["Compliance"] = np.where(synth_df["Compliance_Flag"] == 1, "Yes", "No")
    synth_df = clean_procurement(synth_df.rename(columns={"Compliance": "Compliance"}))
    combined = pd.concat([procurement, synth_df], axis=0, ignore_index=True)
    combined = combined.drop_duplicates(subset=["PO_ID"])
    return combined.reset_index(drop=True)


def run() -> None:
    ensure_processed_dir()

    procurement_raw = pd.read_csv(PROCUREMENT_PATH)
    logistics_raw = pd.read_csv(LOGISTICS_PATH)

    procurement_clean = clean_procurement(procurement_raw)
    logistics_clean = clean_logistics(logistics_raw)
    logistics_agg = aggregate_logistics(logistics_clean)

    procurement_synth = synthesize_procurement_records(procurement_clean, target_size=5000)
    unified = merge_procurement_and_logistics(procurement_synth, logistics_agg)

    procurement_clean.to_csv(CLEANED_PROCUREMENT_PATH, index=False)
    logistics_clean.to_csv(CLEANED_LOGISTICS_PATH, index=False)
    procurement_synth.to_csv(SYNTHETIC_PROCUREMENT_PATH, index=False)
    unified.to_csv(UNIFIED_PATH, index=False)

    print(f"Processed procurement data saved to: {CLEANED_PROCUREMENT_PATH}")
    print(f"Processed logistics data saved to: {CLEANED_LOGISTICS_PATH}")
    print(f"Synthetic procurement dataset saved to: {SYNTHETIC_PROCUREMENT_PATH}")
    print(f"Unified procurement + logistics dataset saved to: {UNIFIED_PATH}")


if __name__ == "__main__":
    run()
