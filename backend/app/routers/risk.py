from pathlib import Path
from typing import Any, Dict, Optional

import joblib
import pandas as pd
from fastapi import APIRouter, Query


def build_automation_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    po_id = payload.get('po_id', 'UNKNOWN')
    anomaly_score = float(payload.get('anomaly_score', 0.0) or 0.0)
    delay_probability = float(payload.get('delay_probability', 0.0) or 0.0)
    priority = 'high' if max(anomaly_score, delay_probability) >= 0.75 else 'medium'
    supplier = payload.get('supplier', 'Unknown')
    item_category = payload.get('item_category', 'Unknown')

    return {
        'event_type': 'PROCUREMENT_RISK_ALERT',
        'workflow_id': f"ARGUS-{po_id}",
        'po_id': po_id,
        'source_system': 'ARGUS',
        'target_system': 'SAP_S4HANA',
        'priority': priority,
        'business_context': {
            'purchase_order': po_id,
            'supplier': supplier,
            'item_category': item_category,
            'company_code': 'US01',
            'currency': 'USD',
        },
        'risk_scores': {
            'price_anomaly_score': round(anomaly_score, 4),
            'delay_probability': round(delay_probability, 4),
        },
        'recommended_actions': [
            {
                'action_code': 'BLOCK_PAYMENT',
                'system': 'SAP',
                'description': 'Place the purchase order on temporary payment hold pending review.',
                'status': 'pending',
            },
            {
                'action_code': 'NOTIFY_SUPPLIER',
                'system': 'S4HANA',
                'description': 'Create a supplier communication task with the latest ETA concerns.',
                'status': 'pending',
            },
            {
                'action_code': 'ESCALATE_PROCUREMENT',
                'system': 'Ariba',
                'description': 'Escalate the purchase order to procurement leadership for remediation.',
                'status': 'pending',
            },
        ],
        'sap_actions': [
            {
                'action': 'hold_payment',
                'system': 'SAP',
                'description': 'Place the purchase order on temporary payment hold pending review.',
            },
            {
                'action': 'notify_supplier',
                'system': 'S4HANA',
                'description': 'Create a supplier communication task with the latest ETA concerns.',
            },
            {
                'action': 'escalate_to_procurement',
                'system': 'Ariba',
                'description': 'Escalate the purchase order to procurement leadership for remediation.',
            },
        ],
        'webhook': {
            'endpoint': '/api/automation/webhook',
            'method': 'POST',
            'status': 'ready',
        },
        'timestamp': payload.get('timestamp') or '2026-08-03T00:00:00Z',
    }


def build_chatbot_reply(message: str) -> Dict[str, Any]:
    normalized = (message or '').strip().lower()
    if 'delay' in normalized or 'risk' in normalized:
        reply = (
            'I recommend reviewing the supplier lead time, confirming shipment readiness, '
            'and escalating the order if the delay probability stays above 0.75.'
        )
    elif 'price' in normalized or 'anomaly' in normalized:
        reply = (
            'I suggest holding the PO for approval, comparing it with negotiated pricing, '
            'and preparing a supplier escalation if the variance remains material.'
        )
    else:
        reply = (
            'I can help you triage a purchase order by summarizing the anomaly score, '
            'delay probability, and the recommended remediation steps.'
        )

    return {
        'reply': reply,
        'status': 'ready',
    }

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


@router.post('/automation/payload')
def automation_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return build_automation_payload(payload)


@router.post('/automation/webhook')
def automation_webhook(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'status': 'accepted',
        'message': 'Automation payload received by ARGUS webhook.',
        'payload': payload,
    }


@router.post('/chatbot/ask')
def chatbot_ask(payload: Dict[str, Any]) -> Dict[str, Any]:
    message = payload.get('message', '')
    return build_chatbot_reply(message)


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
