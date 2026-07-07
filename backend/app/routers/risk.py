from pathlib import Path
from typing import Any, Dict, Optional

import joblib
import pandas as pd
from fastapi import APIRouter, Query

from app.optimization import build_remediation_recommendation

router = APIRouter(prefix="/api", tags=["Risk API"])

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / 'data' / 'processed' / 'unified_procurement_logistics.csv'
MODEL_A_PATH = ROOT / 'ml' / 'models' / 'module_a_isolation_forest.joblib'
MODEL_B_CLASSIFIER_PATH = ROOT / 'ml' / 'models' / 'module_b_delay_classifier.joblib'
MODEL_B_REGRESSOR_PATH = ROOT / 'ml' / 'models' / 'module_b_delay_regressor.joblib'


def load_unified_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


@router.get('/price-risk')
def price_risk(po_id: Optional[str] = Query(default=None)) -> Dict[str, Any]:
    df = load_unified_data()
    if po_id is None:
        row = df.iloc[0]
    else:
        row = df[df['PO_ID'] == po_id].iloc[0]

    anomaly_model = joblib.load(MODEL_A_PATH)
    row_features = pd.DataFrame([{
        'Quantity': row['Quantity'],
        'Unit_Price': row['Unit_Price'],
        'Negotiated_Price': row['Negotiated_Price'],
        'supplier_reliability_score': row['supplier_reliability_score'],
        'price_anomaly_score': row['price_anomaly_score'],
    }])
    anomaly_score = float(-anomaly_model.named_steps['isolation_forest'].decision_function(row_features)[0])
    prediction = anomaly_model.predict(row_features)[0] == -1

    return {
        'po_id': row['PO_ID'],
        'is_anomaly': bool(prediction),
        'anomaly_score': round(anomaly_score, 4),
        'supplier': row['Supplier'],
        'item_category': row['item_category'],
    }


@router.get('/delay-risk')
def delay_risk(po_id: Optional[str] = Query(default=None)) -> Dict[str, Any]:
    df = load_unified_data()
    if po_id is None:
        row = df.iloc[0]
    else:
        row = df[df['PO_ID'] == po_id].iloc[0]

    classifier = joblib.load(MODEL_B_CLASSIFIER_PATH)
    regressor = joblib.load(MODEL_B_REGRESSOR_PATH)
    row_features = pd.DataFrame([{
        'supplier_reliability_score': row['supplier_reliability_score'],
        'price_anomaly_score': row['price_anomaly_score'],
        'delay_probability': row['delay_probability'],
        'delivery_time_deviation': row['delivery_time_deviation'],
        'rolling_delay_rate': row['rolling_delay_rate'],
        'price_volatility_index': row['price_volatility_index'],
        'Quantity': row['Quantity'],
        'Unit_Price': row['Unit_Price'],
    }])
    probability = float(classifier.predict_proba(row_features)[0][1])
    predicted_days = float(regressor.predict(row_features)[0])

    return {
        'po_id': row['PO_ID'],
        'delay_probability': round(probability, 4),
        'predicted_delay_days': round(predicted_days, 2),
        'supplier': row['Supplier'],
        'item_category': row['item_category'],
    }


@router.post('/remediation')
def remediation(payload: Dict[str, Any]) -> Dict[str, Any]:
    po_record = payload.get('po_record', {})
    anomaly_score = payload.get('anomaly_score', 0.0)
    delay_probability = payload.get('delay_probability', 0.0)
    return build_remediation_recommendation(po_record, anomaly_score, delay_probability)


@router.get('/summary')
def summary() -> Dict[str, Any]:
    df = load_unified_data()
    high_risk = df[df['price_anomaly_score'] > 0.5].shape[0]
    delay_risk = df[df['delay_probability'] > 0.5].shape[0]
    return {
        'total_purchase_orders': int(len(df)),
        'high_price_risk_orders': int(high_risk),
        'high_delay_risk_orders': int(delay_risk),
    }
