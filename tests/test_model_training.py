from pathlib import Path
import subprocess
import sys


def test_module_training_scripts_create_outputs(tmp_path):
    repo = Path(__file__).resolve().parents[1]

    subprocess.run(
        [sys.executable, str(repo / 'backend' / 'ml' / 'module_a_price_anomaly' / 'train_anomaly_model.py')],
        cwd=repo,
        check=True,
    )
    subprocess.run(
        [sys.executable, str(repo / 'backend' / 'ml' / 'module_b_disruption' / 'train_delay_models.py')],
        cwd=repo,
        check=True,
    )

    expected_files = [
        repo / 'backend' / 'ml' / 'models' / 'module_a_isolation_forest.joblib',
        repo / 'backend' / 'ml' / 'models' / 'module_b_delay_classifier.joblib',
        repo / 'backend' / 'ml' / 'models' / 'module_b_delay_regressor.joblib',
        repo / 'backend' / 'data' / 'processed' / 'module_a_price_risk.csv',
        repo / 'backend' / 'data' / 'processed' / 'module_b_delay_risk.csv',
    ]

    for path in expected_files:
        assert path.exists(), f'Missing expected artifact: {path}'
