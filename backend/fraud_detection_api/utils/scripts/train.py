import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from joblib import dump

# Load processed data
train_data = pd.read_csv('../datasets/preprocessed_train_data.csv')
X_train = train_data[['fraud_probability', 'is_anomaly']]
y_train = train_data['is_fraud']

# Initialize models with class weighting
models = {
    'xgb': XGBClassifier(
        scale_pos_weight=sum(y_train==0)/sum(y_train==1),
        random_state=42,
        eval_metric='logloss'
    ),
    'catboost': CatBoostClassifier(
        auto_class_weights='Balanced',
        random_state=42,
        verbose=0
    ),
    'random_forest': RandomForestClassifier(
        class_weight='balanced',
        random_state=42
    )
}

# Train and save models
with open('../performance/training_log.txt', 'w') as log:
    for name, model in models.items():
        log.write(f"\n=== Training {name} ===\n")
        
        # Cross-validation
        cv_scores = cross_val_score(
            model, X_train, y_train,
            cv=5, scoring='roc_auc'
        )
        log.write(f"CV ROC-AUC: {np.mean(cv_scores):.4f} ± {np.std(cv_scores):.4f}\n")
        
        # Full training
        model.fit(X_train, y_train)
        dump(model, f'model_{name}.joblib')
        log.write(f"Saved as model_{name}.joblib\n")

print("Training completed. Results saved in training_log.txt")