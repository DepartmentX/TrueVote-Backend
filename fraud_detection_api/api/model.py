import joblib
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
import pandas as pd

iso_foret_model = joblib.load('model/isolation_forest_model.pkl')
logistic_regression_model = LogisticRegression()

def stacked_model_predict(data):
    iso_forest_preds = iso_foret_model.predict(data)
    logistic_regression_preds = logistic_regression_model.predict(data)
    meta_dataset = pd.DataFrame({
        'Address': data['Address'],
        'Isolation_Forest_Prediction': iso_forest_preds,
        'Logistic_Regression_Prediction': logistic_regression_preds
    })

    meta_model = XGBClassifier()
    is_fruad = meta_model.predict(meta_dataset)

    if is_fruad[0] == 1:
        return {'Address': data['Address'].values[0], 'is_fraud': True}
    return {'Address': data['Address'].values[0], 'is_fraud': False}