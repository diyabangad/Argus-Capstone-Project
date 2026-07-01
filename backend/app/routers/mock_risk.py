import json
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Query

router = APIRouter(prefix="/mock", tags=["Mock Risk Data"])

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "mock_risk_data.json"


def load_mock_risk_data():
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


@router.get("/risk-summary")
def get_mock_risk_summary(
    vendor: Optional[str] = Query(default=None),
    category: Optional[str] = Query(default=None),
    severity: Optional[str] = Query(default=None),
    min_deviation: Optional[float] = Query(default=None)
):
    records = load_mock_risk_data()

    if vendor:
        records = [r for r in records if r["vendor"].lower() == vendor.lower()]

    if category:
        records = [r for r in records if r["category"].lower() == category.lower()]

    if severity:
        records = [r for r in records if r["severity"].lower() == severity.lower()]

    if min_deviation is not None:
        records = [
            r for r in records
            if r["deviation_percent"] >= min_deviation
        ]

    return {
        "total_records": len(records),
        "records": records
    }