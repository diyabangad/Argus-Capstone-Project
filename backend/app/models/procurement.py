from datetime import date

from sqlalchemy import (
    Boolean,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Vendor(Base):
    __tablename__ = "vendors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    supplier_name: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    reliability_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    reliability_bucket: Mapped[str | None] = mapped_column(String(50), nullable=True)

    purchase_orders: Mapped[list["PurchaseOrder"]] = relationship(
        back_populates="vendor"
    )


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    po_id: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    vendor_id: Mapped[int] = mapped_column(
        ForeignKey("vendors.id"),
        nullable=False
    )

    item_category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    order_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    delivery_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    expected_delivery_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    expected_delivery_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    order_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    order_status_clean: Mapped[str | None] = mapped_column(String(50), nullable=True)

    quantity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unit_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    negotiated_price: Mapped[float | None] = mapped_column(Float, nullable=True)

    defective_units: Mapped[int | None] = mapped_column(Integer, nullable=True)
    compliance_flag: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    defective_rate: Mapped[float | None] = mapped_column(Float, nullable=True)

    vendor: Mapped["Vendor"] = relationship(back_populates="purchase_orders")
    risk_score: Mapped["RiskScore"] = relationship(
        back_populates="purchase_order",
        uselist=False
    )


class RiskScore(Base):
    __tablename__ = "risk_scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    purchase_order_id: Mapped[int] = mapped_column(
        ForeignKey("purchase_orders.id"),
        unique=True,
        nullable=False
    )

    delivery_delay_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    delay_label: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    price_gap: Mapped[float | None] = mapped_column(Float, nullable=True)
    price_gap_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    price_anomaly_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    logistics_eta_variation_hours: Mapped[float | None] = mapped_column(Float, nullable=True)
    logistics_traffic_congestion_level: Mapped[float | None] = mapped_column(Float, nullable=True)
    logistics_warehouse_inventory_level: Mapped[float | None] = mapped_column(Float, nullable=True)
    logistics_weather_condition_severity: Mapped[float | None] = mapped_column(Float, nullable=True)
    logistics_port_congestion_level: Mapped[float | None] = mapped_column(Float, nullable=True)
    logistics_shipping_costs: Mapped[float | None] = mapped_column(Float, nullable=True)
    logistics_delay_probability: Mapped[float | None] = mapped_column(Float, nullable=True)
    logistics_delivery_time_deviation: Mapped[float | None] = mapped_column(Float, nullable=True)

    purchase_order: Mapped["PurchaseOrder"] = relationship(
        back_populates="risk_score"
    )