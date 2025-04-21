import joblib
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
import pandas as pd
import os
from Crypto.Hash import keccak

iso_foret_model = joblib.load('../model/isolation_forest_model.pkl')
# logistic_regression_model = LogisticRegression()     # need to load the actual model
# meta_model = XGBClassifier()

def hash_address(address):
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(address.encode())
    decimal_address = int(keccak_hash.hexdigest(), 16)
    return decimal_address


def pre_process_data(data):
    pre_process_data = data.copy()
    pre_process_data['Address'] = hash_address(pre_process_data['Address'])
    pre_process_data = pd.DataFrame(pre_process_data, index=[0])    
    return pre_process_data


def stacked_model_predict(data):
    pre_processed_data = pre_process_data(data)
    if not data:
        raise ValueError("No data provided for prediction.")    
    iso_forest_preds = iso_foret_model.predict(pre_processed_data)
    # logistic_regression_preds = logistic_regression_model.predict(data)
    
    meta_dataset = pd.DataFrame({
        'Address': data['Address'],
        'Isolation_Forest_Prediction': iso_forest_preds[0],
        # 'Logistic_Regression_Prediction': logistic_regression_preds['FLAG']
    }, index=[0]).to_numpy()

    # is_fraud = meta_model.predict(meta_dataset)

    is_fraud = iso_forest_preds  # Placeholder for the actual meta model prediction, need to update

    if is_fraud[0] == 1:
        return {'Address': data['Address'], 'is_fraud': True}
    return {'Address': data['Address'], 'is_fraud': False}


