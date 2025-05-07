import pandas as pd
from joblib import load
from sklearn.metrics import (
    classification_report,
    roc_auc_score,
    confusion_matrix,
    precision_recall_curve
)
import matplotlib.pyplot as plt

# Load test data
test_data = pd.read_csv('../datasets/preprocessed_test_data.csv')
X_test = test_data[['fraud_probability', 'is_anomaly']]
y_test = test_data['is_fraud']

# Initialize results
results = {}

# Evaluate each model
with open('../performance/model_performance_report.txt', 'w') as report:
    for model_name in ['xgb', 'catboost', 'random_forest']:
        model = load(f'../../model/model_{model_name}.joblib')
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]
        
        # Store metrics
        results[model_name] = {
            'roc_auc': roc_auc_score(y_test, y_proba),
            'classification_report': classification_report(y_test, y_pred)
        }
        
        # Write to report
        report.write(f"\n{'='*50}\n")
        report.write(f"{model_name.upper()} PERFORMANCE\n")
        report.write(f"ROC-AUC: {results[model_name]['roc_auc']:.4f}\n\n")
        report.write("Classification Report:\n")
        report.write(results[model_name]['classification_report'])

        report.write("\nConfusion Matrix:\n")
        cm = confusion_matrix(y_test, y_pred)
        report.write(f"{cm}\n")
        
        # Plot PR curve
        precision, recall, _ = precision_recall_curve(y_test, y_proba)
        plt.plot(recall, precision, label=model_name)

# Save PR curve
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve Comparison')
plt.legend()
plt.savefig('../performance/pr_curve_comparison.png')
plt.close()

print("Evaluation completed. Results saved in model_performance_report.txt")