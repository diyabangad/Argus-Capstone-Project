from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.procurement import PurchaseOrder, RiskScore, Vendor

router = APIRouter(prefix="/api", tags=["Feature Store"])


@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    total_vendors = db.scalar(select(func.count(Vendor.id)))
    total_purchase_orders = db.scalar(select(func.count(PurchaseOrder.id)))
    total_risk_scores = db.scalar(select(func.count(RiskScore.id)))

    high_price_risk = db.scalar(
        select(func.count(RiskScore.id)).where(
            RiskScore.price_anomaly_score >= 0.75
        )
    )

    delayed_orders = db.scalar(
        select(func.count(RiskScore.id)).where(
            RiskScore.delay_label == True
        )
    )

    avg_price_anomaly = db.scalar(
        select(func.avg(RiskScore.price_anomaly_score))
    )

    avg_delay_probability = db.scalar(
        select(func.avg(RiskScore.logistics_delay_probability))
    )

    return {
        "total_vendors": total_vendors,
        "total_purchase_orders": total_purchase_orders,
        "total_risk_scores": total_risk_scores,
        "high_price_risk_orders": high_price_risk,
        "delayed_orders": delayed_orders,
        "average_price_anomaly_score": round(avg_price_anomaly or 0, 4),
        "average_delay_probability": round(avg_delay_probability or 0, 4),
    }


@router.get("/high-risk-purchase-orders")
def get_high_risk_purchase_orders(
    min_price_anomaly_score: float = Query(default=0.75),
    min_delay_probability: float = Query(default=0.80),
    supplier: Optional[str] = Query(default=None),
    item_category: Optional[str] = Query(default=None),
    limit: int = Query(default=20, le=100),
    db: Session = Depends(get_db),
):
    query = (
        select(
            PurchaseOrder.po_id,
            PurchaseOrder.item_category,
            PurchaseOrder.quantity,
            PurchaseOrder.unit_price,
            PurchaseOrder.negotiated_price,
            PurchaseOrder.order_status,
            RiskScore.delivery_delay_days,
            RiskScore.delay_label,
            RiskScore.price_gap,
            RiskScore.price_gap_pct,
            RiskScore.price_anomaly_score,
            RiskScore.logistics_delay_probability,
            Vendor.supplier_name,
            Vendor.reliability_score,
            Vendor.reliability_bucket,
        )
        .join(RiskScore, RiskScore.purchase_order_id == PurchaseOrder.id)
        .join(Vendor, PurchaseOrder.vendor_id == Vendor.id)
        .where(
            (RiskScore.price_anomaly_score >= min_price_anomaly_score)
            | (RiskScore.logistics_delay_probability >= min_delay_probability)
        )
        .limit(limit)
    )

    if supplier:
        query = query.where(Vendor.supplier_name == supplier)

    if item_category:
        query = query.where(PurchaseOrder.item_category == item_category)

    rows = db.execute(query).mappings().all()

    results = []

    for row in rows:
        results.append(
            {
                "po_id": row.po_id,
                "supplier": row.supplier_name,
                "supplier_reliability_score": row.reliability_score,
                "supplier_reliability_bucket": row.reliability_bucket,
                "item_category": row.item_category,
                "quantity": row.quantity,
                "unit_price": row.unit_price,
                "negotiated_price": row.negotiated_price,
                "order_status": row.order_status,
                "delivery_delay_days": row.delivery_delay_days,
                "delay_label": row.delay_label,
                "price_gap": row.price_gap,
                "price_gap_pct": row.price_gap_pct,
                "price_anomaly_score": row.price_anomaly_score,
                "delay_probability": row.logistics_delay_probability,
                "recommended_note": "Review this PO because price anomaly score or delay probability is high.",
            }
        )

    return {
        "total_records": len(results),
        "records": results,
    }


@router.get("/vendor-risk-profile/{supplier_name}")
def get_vendor_risk_profile(
    supplier_name: str,
    db: Session = Depends(get_db),
):
    vendor = db.execute(
        select(
            Vendor.id,
            Vendor.supplier_name,
            Vendor.reliability_score,
            Vendor.reliability_bucket,
        ).where(Vendor.supplier_name == supplier_name)
    ).mappings().one_or_none()

    if not vendor:
        return {
            "message": "Vendor not found",
            "supplier": supplier_name,
        }

    total_orders = db.scalar(
        select(func.count(PurchaseOrder.id)).where(
            PurchaseOrder.vendor_id == vendor.id
        )
    )

    avg_price_anomaly = db.scalar(
        select(func.avg(RiskScore.price_anomaly_score))
        .join(PurchaseOrder, RiskScore.purchase_order_id == PurchaseOrder.id)
        .where(PurchaseOrder.vendor_id == vendor.id)
    )

    avg_delay_probability = db.scalar(
        select(func.avg(RiskScore.logistics_delay_probability))
        .join(PurchaseOrder, RiskScore.purchase_order_id == PurchaseOrder.id)
        .where(PurchaseOrder.vendor_id == vendor.id)
    )

    delayed_orders = db.scalar(
        select(func.count(RiskScore.id))
        .join(PurchaseOrder, RiskScore.purchase_order_id == PurchaseOrder.id)
        .where(
            PurchaseOrder.vendor_id == vendor.id,
            RiskScore.delay_label == True,
        )
    )

    return {
        "supplier": vendor.supplier_name,
        "supplier_reliability_score": vendor.reliability_score,
        "supplier_reliability_bucket": vendor.reliability_bucket,
        "total_orders": total_orders,
        "delayed_orders": delayed_orders,
        "average_price_anomaly_score": round(avg_price_anomaly or 0, 4),
        "average_delay_probability": round(avg_delay_probability or 0, 4),
    }
