from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_absolute_error
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / 'data' / 'processed' / 'unified_procurement_logistics.csv'
OUTPUT_PATH = ROOT / 'data' / 'processed' / 'module_b_delay_risk.csv'
CLASSIFIER_PATH = ROOT / 'ml' / 'models' / 'module_b_delay_classifier.joblib'
REGRESSOR_PATH = ROOT / 'ml' / 'models' / 'module_b_delay_regressor.joblib'


def train_and_save():
    df = pd.read_csv(DATA_PATH)
    features = [
        'supplier_reliability_score',
        'price_anomaly_score',
        'delay_probability',
        'delivery_time_deviation',
        'rolling_delay_rate',
        'price_volatility_index',
        'Quantity',
        'Unit_Price',
    ]
    target = 'Delay_Label'
    model_df = df[features + [target]].dropna().copy()

    X_train, X_test, y_train, y_test = train_test_split(model_df[features], model_df[target], test_size=0.2, random_state=42)

    classifier = RandomForestClassifier(n_estimators=120, random_state=42)
    classifier.fit(X_train, y_train)
    class_pred = classifier.predict(X_test)
    print('classifier_accuracy', accuracy_score(y_test, class_pred))

    regressor = RandomForestRegressor(n_estimators=120, random_state=42)
    regressor.fit(X_train, y_train)
    reg_pred = regressor.predict(X_test)
    print('regressor_mae', mean_absolute_error(y_test, reg_pred))

    df['delay_risk_probability'] = classifier.predict_proba(model_df[features])[:, 1]
    df['predicted_delay_days'] = regressor.predict(model_df[features])
    df[['PO_ID', 'delay_risk_probability', 'predicted_delay_days']].to_csv(OUTPUT_PATH, index=False)

    CLASSIFIER_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(classifier, CLASSIFIER_PATH)
    joblib.dump(regressor, REGRESSOR_PATH)
    print(f'Saved classifier to {CLASSIFIER_PATH}')
    print(f'Saved regressor to {REGRESSOR_PATH}')
    print(f'Saved delay risk output to {OUTPUT_PATH}')


if __name__ == '__main__':
    train_and_save()
