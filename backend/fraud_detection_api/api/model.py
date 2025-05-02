import joblib
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
import pandas as pd
import os
from Crypto.Hash import keccak
from schema import ElectionFraudDetectionRequest

iso_foret_model = joblib.load('../model/isolation_forest_model.pkl')
logistic_regression_model = joblib.load('../model/logistic_regression_model.pkl')
meta_model = joblib.load('../model/model_xgb.joblib')

def hash_address(address):
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(address.encode())
    decimal_address = int(keccak_hash.hexdigest(), 16)
    return decimal_address


def pre_process_data(data):
    pre_process_data = data.copy().dict(by_alias=True)
    pre_process_data['Address'] = hash_address(pre_process_data['Address'])
    pre_process_data = pd.DataFrame([pre_process_data])
    return pre_process_data


def stacked_model_predict(data):
    pre_processed_data = pre_process_data(data)
    print(pre_processed_data.columns)

    if not data:
        raise ValueError("No data provided for prediction.")
    
    iso_forest_preds = iso_foret_model.predict(pre_processed_data)
    logistic_regression_preds = logistic_regression_model.predict_proba(pre_processed_data.drop(columns=['Address']).to_numpy())
    
    meta_dataset = pd.DataFrame({
        'is_anomaly': iso_forest_preds[0],
        'fraud_probability': logistic_regression_preds[0][1],
    }, index=[0]).to_numpy()

    is_fraud = meta_model.predict(meta_dataset)

    if is_fraud[0] == 1:
        return {'Address': data.Address, 'is_fraud': True}
    return {'Address': data.Address, 'is_fraud': False}


