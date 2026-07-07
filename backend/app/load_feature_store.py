from pathlib import Path

import pandas as pd
from sqlalchemy import delete

from app.core.database import Base, SessionLocal, engine
from app.models.procurement import PurchaseOrder, RiskScore, Vendor


CSV_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "processed"
    / "unified_procurement_logistics.csv"
)


def clean_value(value):
    if pd.isna(value):
        return None
    return value


def clean_date(value):
    if pd.isna(value):
        return None
    return pd.to_datetime(value).date()


def load_feature_store():
    Base.metadata.create_all(bind=engine)

    df = pd.read_csv(CSV_PATH)

    with SessionLocal() as db:
        # Clear old data so rerunning this script does not create duplicates
        db.execute(delete(RiskScore))
        db.execute(delete(PurchaseOrder))
        db.execute(delete(Vendor))
        db.commit()

        vendors = {}

        for _, row in df.iterrows():
            supplier_name = str(row["Supplier"])

            if supplier_name not in vendors:
                vendor = Vendor(
                    supplier_name=supplier_name,
                    reliability_score=clean_value(
                        row["Supplier_Reliability_Score"]
                    ),
                    reliability_bucket=clean_value(
                        row["Supplier_Reliability_Bucket"]
                    ),
                    material_group=clean_value(row["material_group"]),
                )
                vendors[supplier_name] = vendor
                db.add(vendor)

            purchase_order = PurchaseOrder(
                po_id=str(row["PO_ID"]),
                vendor=vendors[supplier_name],
                item_category=clean_value(row["item_category"]),
                material_group=clean_value(row["material_group"]),
                vendor_id=clean_value(row["vendor_id"]),
                order_date=clean_date(row["Order_Date"]),
                delivery_date=clean_date(row["Delivery_Date"]),
                expected_delivery_date=clean_date(
                    row["Expected_Delivery_Date"]
                ),
                expected_delivery_days=clean_value(
                    row["Expected_Delivery_Days"]
                ),
                order_status=clean_value(row["Order_Status"]),
                order_status_clean=clean_value(row["Order_Status_Clean"]),
                quantity=clean_value(row["Quantity"]),
                unit_price=clean_value(row["Unit_Price"]),
                negotiated_price=clean_value(row["Negotiated_Price"]),
                defective_units=clean_value(row["Defective_Units"]),
                compliance_flag=bool(row["Compliance_Flag"]),
                defective_rate=clean_value(row["Defective_Rate"]),
            )

            risk_score = RiskScore(
                purchase_order=purchase_order,
                delivery_delay_days=clean_value(
                    row["Delivery_Delay_Days"]
                ),
                delay_label=bool(row["Delay_Label"]),
                price_gap=clean_value(row["Price_Gap"]),
                price_gap_pct=clean_value(row["Price_Gap_Pct"]),
                price_gap_anomaly_score=clean_value(
                    row["Price_Anomaly_Score"]
                ),
                logistics_eta_variation_hours=clean_value(
                    row["logistics_median_eta_variation_hours"]
                ),
                logistics_traffic_congestion_level=clean_value(
                    row["logistics_median_traffic_congestion_level"]
                ),
                logistics_warehouse_inventory_level=clean_value(
                    row["logistics_median_warehouse_inventory_level"]
                ),
                logistics_weather_condition_severity=clean_value(
                    row["logistics_median_weather_condition_severity"]
                ),
                logistics_port_congestion_level=clean_value(
                    row["logistics_median_port_congestion_level"]
                ),
                logistics_shipping_costs=clean_value(
                    row["logistics_median_shipping_costs"]
                ),
                logistics_delay_probability=clean_value(
                    row["logistics_median_delay_probability"]
                ),
                logistics_delivery_time_deviation=clean_value(
                    row["logistics_median_delivery_time_deviation"]
                ),
                supplier_reliability_score=clean_value(
                    row["supplier_reliability_score"]
                ),
                price_anomaly_score=clean_value(
                    row["price_anomaly_score"]
                ),
                delay_probability=clean_value(
                    row["delay_probability"]
                ),
                delivery_time_deviation=clean_value(
                    row["delivery_time_deviation"]
                ),
                rolling_delay_rate=clean_value(
                    row["rolling_delay_rate"]
                ),
                price_volatility_index=clean_value(
                    row["price_volatility_index"]
                ),
            )

            db.add(purchase_order)
            db.add(risk_score)

        db.commit()

    print(f"Loaded {len(df)} purchase orders into the ARGUS feature store.")
    print(f"Loaded {len(vendors)} vendors.")


if __name__ == "__main__":
    load_feature_store()