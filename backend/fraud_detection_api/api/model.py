import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import RobustScaler
from xgboost import XGBClassifier
import pandas as pd
import os
from Crypto.Hash import keccak

iso_foret_model = joblib.load('../model/isolation_forest_model.pkl')
logistic_regression_model = joblib.load('../model/logistic_regression_model.pkl')
meta_model = joblib.load('../model/model_xgb.joblib')



def hash_address(address):
    if not isinstance(address, str):
        raise ValueError("Address must be a non-null string.")
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(address.encode())
    decimal_address = int(keccak_hash.hexdigest(), 16)
    normalized_address = decimal_address / (2**256 - 1)
    return normalized_address


def pre_process_data(data):
    pre_process_data = data.copy().dict(by_alias=True)
    pre_process_data = pd.DataFrame([pre_process_data])
    pre_process_data['Address'] = pre_process_data['Address'].apply(hash_address)

    robust_scaler_path = '../utils/robust_scaler.joblib'  
    robust_scaler = joblib.load(robust_scaler_path)
    
    try:
        for col in pre_process_data.columns:
            pre_process_data[col] = robust_scaler.transform(pre_process_data[col].values.reshape(-1, 1))
    except Exception as e:
        print("Error during scaling:", str(e))
        raise

    pre_process_data = pd.DataFrame(pre_process_data, columns=pre_process_data.columns)

    return pre_process_data

def scale_data(data):
    scaler = joblib.load('../utils/feature_scaler.joblib')
    scaled_data = scaler.transform(data)
    return scaled_data

def stacked_model_predict(data):
    pre_processed_data = pre_process_data(data)

    if not data:
        raise ValueError("No data provided for prediction.")
    
    iso_forest_preds = iso_foret_model.predict(pre_processed_data)
    logistic_regression_preds = logistic_regression_model.predict_proba(pre_processed_data.drop(columns=['Address']))

    # print("Fraud Probability: ", logistic_regression_preds[0][1], '\n', "Anomaly score: ", iso_forest_preds[0])

    meta_dataset = pd.DataFrame({
        'fraud_probability': logistic_regression_preds[0][1],
        'is_anomaly': 1 if iso_forest_preds[0] == -1 else 0,
    }, index=[0])[['fraud_probability', 'is_anomaly']]

    expected_columns = ['fraud_probability', 'is_anomaly']
    for col in expected_columns:
        if col not in meta_dataset.columns:
            meta_dataset[col] = 0 

    meta_dataset = scale_data(meta_dataset)
    # print("Fraud Probability: ", meta_dataset[0][0], '\n', "Anomaly score: ", meta_dataset[0][1])

    is_fraud = meta_model.predict(meta_dataset)
    print(is_fraud[0])

    if is_fraud[0] == 1:
        return {'Address': data.Address, 'is_fraud': True}
    return {'Address': data.Address, 'is_fraud': False}


