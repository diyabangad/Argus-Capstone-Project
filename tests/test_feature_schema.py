from pathlib import Path
import subprocess
import sys

import pandas as pd


def test_preprocessing_outputs_shared_feature_columns():
    repo = Path(__file__).resolve().parents[1]
    subprocess.run(
        [sys.executable, str(repo / 'backend' / 'ml' / 'prepare_procurement_logistics_dataset.py')],
        cwd=repo,
        check=True,
    )

    unified = pd.read_csv(repo / 'backend' / 'data' / 'processed' / 'unified_procurement_logistics.csv')

    required_cols = [
        'vendor_id',
        'material_group',
        'item_category',
        'supplier_reliability_score',
        'price_anomaly_score',
        'delay_probability',
        'delivery_time_deviation',
        'rolling_delay_rate',
        'price_volatility_index',
    ]

    missing = [col for col in required_cols if col not in unified.columns]
    assert not missing, f'Missing columns: {missing}'
