from __future__ import annotations

from typing import Any, Dict


def _score_severity(anomaly_score: float, delay_probability: float) -> float:
    return float(anomaly_score * 0.6 + delay_probability * 0.4)


def build_remediation_recommendation(po_record: Dict[str, Any], anomaly_score: float, delay_probability: float) -> Dict[str, Any]:
    anomaly_score = float(anomaly_score or 0.0)
    delay_probability = float(delay_probability or 0.0)
    severity = _score_severity(anomaly_score, delay_probability)

    supplier = po_record.get('Supplier') or po_record.get('supplier') or 'Unknown'
    item_category = po_record.get('Item_Category') or po_record.get('item_category') or 'Unknown'

    if severity >= 0.85:
        action = 'backup_vendor'
        rationale = 'The combined price and delay risk is very high, so a backup supplier and order revalidation are the best tradeoff.'
        expected_cost = 'high'
    elif anomaly_score >= 0.7 and delay_probability >= 0.5:
        action = 'renegotiate'
        rationale = 'Price risk is elevated and delay risk is meaningful, so renegotiation is preferable to a costly expedite decision.'
        expected_cost = 'medium'
    elif delay_probability >= 0.7:
        action = 'expedite_shipping'
        rationale = 'Delay risk is dominant, and expedited shipping is the most cost-effective way to reduce disruption exposure.'
        expected_cost = 'medium'
    elif anomaly_score >= 0.7:
        action = 'renegotiate'
        rationale = 'Price variance is high enough to justify renegotiation before approval.'
        expected_cost = 'low'
    else:
        action = 'monitor'
        rationale = 'Risk is moderate, so the best action is to monitor the order and keep a fallback option ready.'
        expected_cost = 'low'

    return {
        'po_id': po_record.get('PO_ID') or po_record.get('po_id') or 'unknown',
        'supplier': supplier,
        'item_category': item_category,
        'anomaly_score': round(anomaly_score, 4),
        'delay_probability': round(delay_probability, 4),
        'severity_score': round(severity, 4),
        'recommended_action': action,
        'expected_cost': expected_cost,
        'rationale': rationale,
    }
