import pytest
import os
import sys
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.utils.model import hash_address

def generate_eth_address():
    return "0x" + ''.join(random.choices('0123456789abcdefABCDEF', k=40))

@pytest.mark.parametrize("i", range(10))  # Run 10 tests with different data
def test_hash_address_function(i):
    log_file = "../../app/utils/performance/test_hash_address_results.txt"
    with open(log_file, "a") as log:
        eth_address = generate_eth_address()

        log.write(f"\nTest case {i+1}:\n")
        log.write(f"Ethereum Address: {eth_address}\n")

        try:
            hashed_address = str(hash_address(eth_address))
            log.write(f"Hashed Address: {hashed_address}\n")

            # Assertions to validate the hashed address
            assert isinstance(hashed_address, str), "Hashed address is not a string"
            assert len(hashed_address) > 0, "Hashed address is empty"
            assert eth_address != hashed_address, "Hashed address should not match the original address"

            log.write("Test passed.\n")
        except AssertionError as e:
            log.write(f"Test failed: {e}\n")
            pytest.fail(f"Test case {i+1} failed: {e}")
