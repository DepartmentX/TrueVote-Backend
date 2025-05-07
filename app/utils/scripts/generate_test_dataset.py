import pandas as pd
import random


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


data = [generate_row() for _ in range(2000)]

df = pd.DataFrame(data)

df.to_csv("../datasets/test_data.csv", index=False)

print("✅ Dataset with 2000 rows saved to 'test_data.csv'")
