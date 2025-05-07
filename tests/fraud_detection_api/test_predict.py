import pytest
import os
import sys
import pandas as pd
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.utils.model import stacked_model_predict

def extract_input_and_output(row):
    features = pd.DataFrame([{
        "Address": row["Address"],
        "Time Diff between first and last (Mins)": row["Time Diff between first and last (Mins)"],
        "Face Attempts": row["Face Attempts"],
        "Detected As a Robot At Least Once": row["Detected As a Robot At Least Once"],
        "Face Match Percentage": row["Face Match Percentage"],
        "Liveness Score of The Face": row["Liveness Score of The Face"]
    }])
    return features, row["is_fraud"]


def generate_eth_address():
    return "0x" + ''.join(random.choices('0123456789abcdefABCDEF', k=40))


def generate_row():
    face_match = round(random.uniform(30.0, 100.0), 1)
    liveness = round(random.uniform(30.0, 100.0), 1)
    robot_flag = random.randint(0, 1)
    if random.random() < 0.85:
        time_diff = round(random.uniform(1, 60), 1)
    else:
        time_diff = round(random.uniform(60, 100000), 1)
    attempts = random.randint(1, 3)

    # Scoring-based fraud logic (non-obvious)
    score = 0
    if robot_flag == 1: score += 2
    if face_match < 75: score += 1
    if liveness < 60: score += 1
    if attempts > 2: score += 1
    if time_diff > 60: score += 1

    is_fraud = 1 if score >= 3 else 0

    # # Add 5% noise
    # if random.random() < 0.05:
    #     is_fraud = 1 - is_fraud

    return {
        "Address": generate_eth_address(),
        "Time Diff between first and last (Mins)": time_diff,
        "Face Attempts": attempts,
        "Detected As a Robot At Least Once": robot_flag,
        "Face Match Percentage": face_match,
        "Liveness Score of The Face": liveness,
        "is_fraud": is_fraud,
    }

@pytest.mark.parametrize("i", range(10))  # Run 10 tests with different data
def test_generated_rows(i):
    log_file = "../../app/utils/performance/test_predict_results.txt"
    with open(log_file, "a") as log:
        row = generate_row()
        features, output = extract_input_and_output(row)

        log.write(f"\nTest case {i+1}:\n")
        log.write(f"Row: {row}\n")
        log.write(f"Features: {features}\n")
        log.write(f"Expected output: {output}\n")

        try:
            assert isinstance(output, int), f"Expected output to be int, got {type(output)}"
            assert output in [0, 1], f"Expected output to be 0 or 1, got {output}"
            assert isinstance(features, pd.DataFrame), "Features is not a DataFrame"
            assert features.shape == (1, 6), f"Expected features shape (1,6), got {features.shape}"

            prediction = stacked_model_predict(features)['is_fraud']
            log.write(f"Prediction: {prediction}\n")
            assert prediction in [0, 1], f"Prediction should be 0 or 1, but got {prediction}"

            log.write("Test passed.\n")
        except AssertionError as e:
            log.write(f"Test failed: {e}\n")
            pytest.fail(f"Test case {i+1} failed: {e}")
