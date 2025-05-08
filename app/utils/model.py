import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import RobustScaler
from xgboost import XGBClassifier
import pandas as pd
import os
from Crypto.Hash import keccak

iso_foret_model = joblib.load('./models/isolation_forest_model.pkl')    # Use ../../models/isolation_forest_model.pkl when doing unit tests
logistic_regression_model = joblib.load('./models/logistic_regression_model.pkl')    # Use ../../models/logistic_regression_model.pkl when doing unit tests
meta_model = joblib.load('./models/model_xgb.joblib')     # Use ../../models/model_xgb.joblib when doing unit tests



def hash_address(address):
    print("Hashing address:", address)

    if not isinstance(address, str):
        print("Invalid address type:", type(address))
        raise ValueError("Address must be a non-null string.")
    keccak_hash = keccak.new(digest_bits=256)

    try:
        keccak_hash.update(address.encode())
    except Exception as e:
        print("Error during hashing:", str(e))
        raise

    decimal_address = int(keccak_hash.hexdigest(), 16)

    try:
        normalized_address = decimal_address / (2**256 - 1)
    except ZeroDivisionError:
        print("Error during normalization:", str(e))
        raise
    except Exception as e:
        print("Error during normalization:", str(e))
        raise

    return normalized_address


def pre_process_data(data):
    pre_process_data = data.copy()
    pre_process_data = pd.DataFrame(pre_process_data)

    print("Columns available:", pre_process_data.columns)

    try:
        pre_process_data['Address'] = pre_process_data['Address'].apply(hash_address)
    except Exception as e:
        print("Error during address hashing:", e)
        raise

    robust_scaler_path = './app/utils/feature_scalers/robust_scaler.joblib'      # Use ../../app/utils/feature_scalers/robust_scaler.joblib when doing unit tests
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
    scaler = joblib.load('./app/utils/feature_scalers/feature_scaler.joblib')      # Use ../../app/utils/feature_scalers/feature_scaler.joblib when doing unit tests
    scaled_data = scaler.transform(data)
    return scaled_data

def stacked_model_predict(data):
    pre_processed_data = pre_process_data(data)

    if data is None or data.empty:
        raise ValueError("No data provided for prediction.")
    
    iso_forest_preds = iso_foret_model.predict(pre_processed_data)
    logistic_regression_preds = logistic_regression_model.predict_proba(pre_processed_data.drop(columns=['Address']))

    # print("Fraud Probability: ", logistic_regression_preds[0][1], '\n', "Anomaly score: ", iso_forest_preds[0])

    meta_dataset = pd.DataFrame({
        'fraud_probability': logistic_regression_preds[:, 1],
        'is_anomaly': [1 if pred == -1 else 0 for pred in iso_forest_preds],
    })

    expected_columns = ['fraud_probability', 'is_anomaly']
    for col in expected_columns:
        if col not in meta_dataset.columns:
            meta_dataset[col] = 0 

    meta_dataset = scale_data(meta_dataset)
    # print("Fraud Probability: ", meta_dataset[0][0], '\n', "Anomaly score: ", meta_dataset[0][1])

    is_fraud = meta_model.predict(meta_dataset)
    print(is_fraud[0])

    return {'Address': data.Address, 'is_fraud': is_fraud}


