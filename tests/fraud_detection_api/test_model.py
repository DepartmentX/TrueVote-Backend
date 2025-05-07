import pandas as pd
from joblib import load
from sklearn.metrics import (
    classification_report,
    roc_auc_score,
    confusion_matrix,
    precision_recall_curve
)
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.utils.model import stacked_model_predict

# Load test data
test_data = pd.read_csv('../../app/utils/datasets/test_data.csv')
X_test = test_data.drop(columns=['is_fraud'])
y_test = test_data['is_fraud']

# Initialize results
results = {}

# Evaluate each model
with open('../../app/utils/performance/model_test_report.txt', 'w') as report:
    y_pred = stacked_model_predict(X_test)
    
    # Store metrics
    results = {
        'roc_auc': roc_auc_score(y_test, y_pred['is_fraud']),
        'classification_report': classification_report(y_test, y_pred['is_fraud'])
    }
    
    # Write to report
    report.write(f"\n{'='*50}\n")
    report.write(f"TESTING PERFORMANCE\n")
    report.write(f"ROC-AUC: {results['roc_auc']:.4f}\n\n")
    report.write("Classification Report:\n")
    report.write(results['classification_report'])

    report.write("\nConfusion Matrix:\n")
    cm = confusion_matrix(y_test, y_pred['is_fraud'])
    report.write(f"{cm}\n")
    
    # Plot PR curve
    precision, recall, _ = precision_recall_curve(y_test, y_pred['is_fraud'])
    plt.figure(figsize=(8, 6))
    plt.plot(recall, precision, label='test_performance')

# Save PR curve
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve Comparison')
plt.legend()
plt.savefig('../../app/utils/performance/pr_curve_test.png')
plt.close()

print("Evaluation completed. Results saved in model_performance_report.txt")