from __future__ import annotations

from typing import Any, Dict


def build_remediation_recommendation(po_record: Dict[str, Any], anomaly_score: float, delay_probability: float) -> Dict[str, Any]:
    anomaly_score = float(anomaly_score or 0.0)
    delay_probability = float(delay_probability or 0.0)

    if anomaly_score >= 0.7 and delay_probability >= 0.7:
        action = 'backup_vendor'
        rationale = 'High price anomaly and high delay risk suggest switching to a backup supplier and revalidating the purchase order.'
    elif anomaly_score >= 0.7:
        action = 'renegotiate'
        rationale = 'Price variance is high enough to justify price renegotiation before approval.'
    elif delay_probability >= 0.7:
        action = 'expedite_shipping'
        rationale = 'The shipment is likely to be delayed, so expedite handling and supplier follow-up are recommended.'
    else:
        action = 'monitor'
        rationale = 'Risk is moderate; monitor the order closely and keep a fallback plan ready.'

    supplier = po_record.get('Supplier') or po_record.get('supplier') or 'Unknown'
    item_category = po_record.get('Item_Category') or po_record.get('item_category') or 'Unknown'

    return {
        'po_id': po_record.get('PO_ID') or po_record.get('po_id') or 'unknown',
        'supplier': supplier,
        'item_category': item_category,
        'anomaly_score': round(anomaly_score, 4),
        'delay_probability': round(delay_probability, 4),
        'recommended_action': action,
        'rationale': rationale,
    }
