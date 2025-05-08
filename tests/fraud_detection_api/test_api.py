import pytest
import requests
import time
import random

BASE_URL = "http://127.0.0.1:8000/validate_vote/"

def generate_payload():
    return {
        "Address": "0x" + ''.join(random.choices("0123456789abcdef", k=40)),
        "Time Diff between first and last (Mins)": random.uniform(0, 120),
        "Face Attempts": random.randint(1, 3),
        "Detected As a Robot At Least Once": random.randint(0, 1),
        "Face Match Percentage": random.uniform(30, 100),
        "Liveness Score of The Face": random.uniform(30, 100)
    }

@pytest.mark.parametrize("i", range(10))  # Run 10 tests with different data
def test_validate_vote_endpoint(i):
    payload = generate_payload()
    start = time.time()
    response = requests.post(BASE_URL, json=payload)

    response_data = response.json()
    elapsed = time.time() - start

    assert response.status_code == 200, f"Failed with payload: {payload}"

    data = response_data
    assert "Address" in data
    assert "is_fraud" in data
    assert isinstance(data["is_fraud"], int)
    assert data["Address"].startswith("0x")

    test_status = "PASSED" if response.status_code == 200 and "Address" in data and "is_fraud" in data and isinstance(data["is_fraud"], int) and data["Address"].startswith("0x") else "FAILED"
    
    with open("../../app/utils/performance/endpoint_test_results.txt", "a") as file:
        file.write(f"Test {i+1}:\n")
        file.write(f"Payload: {payload}\n")
        file.write(f"Response: {response_data}\n")
        file.write(f"Elapsed Time: {elapsed:.3f} sec\n")
        file.write(f"Is Fraud: {data['is_fraud']}\n")
        file.write(f"Test Status: {str(test_status)}\n")
        file.write("-" * 50 + "\n")

    print(f"Test {i+1}: {elapsed:.3f} sec, is_fraud = {data['is_fraud']}")
