import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from joblib import dump

# Load and rename columns
df = pd.read_csv('../datasets/meta_model_train_dataset.csv').rename(columns={
    'Anomaly': 'is_anomaly',
    'FLAG': 'is_fraud'
})

# Verify data
print("Data Overview:")
print(f"Shape: {df.shape}")
print(f"Fraud Rate: {df['is_fraud'].mean():.2%}")

# Feature-target split
X = df[['fraud_probability', 'is_anomaly']]
y = df['is_fraud']

# Train-test split (70-30 stratified)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.3, 
    random_state=42,
    stratify=y
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save processed data
pd.concat([
    pd.DataFrame(X_train_scaled, columns=X.columns),
    y_train.reset_index(drop=True)
], axis=1).to_csv('../datasets/preprocessed_train_data.csv', index=False)

pd.concat([
    pd.DataFrame(X_test_scaled, columns=X.columns),
    y_test.reset_index(drop=True)
], axis=1).to_csv('../datasets/preprocessed_test_data.csv', index=False)

# Save scaler
dump(scaler, '../feature_scaler.joblib')

print("\nPreprocessing completed:")
print(f"- Training samples: {len(X_train)}")
print(f"- Test samples: {len(X_test)}")
print("- Scaler saved as feature_scaler.joblib")