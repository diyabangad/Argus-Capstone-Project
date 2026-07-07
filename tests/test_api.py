from pathlib import Path
import sys

import pandas as pd
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1] / 'backend'))

from app.main import app


client = TestClient(app)


def test_price_risk_endpoint_returns_payload():
    unified = pd.read_csv(Path(__file__).resolve().parents[1] / 'backend' / 'data' / 'processed' / 'unified_procurement_logistics.csv')
    po_id = unified.iloc[0]['PO_ID']

    response = client.get('/api/price-risk', params={'po_id': po_id})
    assert response.status_code == 200
    payload = response.json()
    assert payload['po_id'] == po_id
    assert 'is_anomaly' in payload
    assert 'anomaly_score' in payload


def test_delay_risk_endpoint_returns_payload():
    unified = pd.read_csv(Path(__file__).resolve().parents[1] / 'backend' / 'data' / 'processed' / 'unified_procurement_logistics.csv')
    po_id = unified.iloc[0]['PO_ID']

    response = client.get('/api/delay-risk', params={'po_id': po_id})
    assert response.status_code == 200
    payload = response.json()
    assert payload['po_id'] == po_id
    assert 'delay_probability' in payload
    assert 'predicted_delay_days' in payload


def test_remediation_endpoint_returns_recommendation():
    payload = {
        'po_record': {'PO_ID': 'PO-00001', 'Supplier': 'Alpha_Inc', 'Item_Category': 'MRO'},
        'anomaly_score': 0.8,
        'delay_probability': 0.75,
    }

    response = client.post('/api/remediation', json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body['recommended_action'] in {'renegotiate', 'expedite_shipping', 'backup_vendor', 'monitor'}
    assert 'severity_score' in body
    assert 'expected_cost' in body
