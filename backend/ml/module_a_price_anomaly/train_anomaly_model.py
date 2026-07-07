from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / 'data' / 'processed' / 'unified_procurement_logistics.csv'
OUTPUT_PATH = ROOT / 'data' / 'processed' / 'module_a_price_risk.csv'
MODEL_PATH = ROOT / 'ml' / 'models' / 'module_a_isolation_forest.joblib'


def train_and_save():
    df = pd.read_csv(DATA_PATH)
    features = [
        'Quantity',
        'Unit_Price',
        'Negotiated_Price',
        'supplier_reliability_score',
        'price_anomaly_score',
    ]
    model_df = df[features].dropna().copy()

    numeric_features = ['Quantity', 'Unit_Price', 'Negotiated_Price', 'supplier_reliability_score', 'price_anomaly_score']
    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), numeric_features),
    ], remainder='drop')

    model = Pipeline([
        ('preprocess', preprocessor),
        ('isolation_forest', IsolationForest(n_estimators=100, contamination=0.05, random_state=42)),
    ])
    model.fit(model_df)

    scores = -model.named_steps['isolation_forest'].decision_function(model_df)
    model_df['anomaly_score'] = scores
    model_df['is_anomaly'] = model.predict(model_df) == -1

    model_df.to_csv(OUTPUT_PATH, index=False)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f'Saved anomaly model to {MODEL_PATH}')
    print(f'Saved risk scores to {OUTPUT_PATH}')


if __name__ == '__main__':
    train_and_save()
