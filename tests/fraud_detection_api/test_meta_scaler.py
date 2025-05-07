import pytest
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.utils.model import scale_data

@patch('app.utils.model.joblib.load')
def test_scale_data(mock_joblib_load):
    mock_scaler = MagicMock()
    mock_scaler.transform.return_value = np.array([[0.5, -1.2], [1.3, 0.7]])
    mock_joblib_load.return_value = mock_scaler

    input_data = np.array([[10, 100], [20, 200]])
    expected_output = np.array([[0.5, -1.2], [1.3, 0.7]])

    output = scale_data(input_data)

    mock_joblib_load.assert_called_once_with('../../app/utils/feature_scalers/feature_scaler.joblib')
    mock_scaler.transform.assert_called_once_with(input_data)
    np.testing.assert_array_equal(output, expected_output)

    try:
        np.testing.assert_array_equal(output, expected_output)
        test_status = "PASSED"
    except AssertionError as e:
        test_status = f"FAILED: {str(e)}"

    with open("../../app/utils/performance/meta_scaler_test_results.txt", "a") as file:
        file.write(f"Test Status: {test_status}\n")
        file.write(f"Input Data:\n {input_data}\n")
        file.write(f"Expected Output:\n {expected_output}\n")
        file.write(f"Actual Output:\n {output}\n")
        file.write("-" * 50 + "\n")


@patch('app.utils.model.joblib.load')
def test_scale_data_empty_input(mock_joblib_load):
    mock_scaler = MagicMock()
    mock_scaler.transform.return_value = np.array([])
    mock_joblib_load.return_value = mock_scaler

    input_data = np.array([])
    expected_output = np.array([])

    output = scale_data(input_data)

    mock_joblib_load.assert_called_once_with('../../app/utils/feature_scalers/feature_scaler.joblib')
    mock_scaler.transform.assert_called_once_with(input_data)
    np.testing.assert_array_equal(output, expected_output)

    try:
        np.testing.assert_array_equal(output, expected_output)
        test_status = "PASSED"
    except AssertionError as e:
        test_status = f"FAILED: {str(e)}"

    with open("../../app/utils/performance/meta_scaler_test_results.txt", "a") as file:
        file.write(f"Test Status: {test_status}\n")
        file.write(f"Input Data:\n {input_data}\n")
        file.write(f"Expected Output:\n {expected_output}\n")
        file.write(f"Actual Output:\n {output}\n")
        file.write("-" * 50 + "\n")


@patch('app.utils.model.joblib.load')
def test_scale_data_single_row(mock_joblib_load):
    mock_scaler = MagicMock()
    mock_scaler.transform.return_value = np.array([[0.1, -0.2]])
    mock_joblib_load.return_value = mock_scaler

    input_data = np.array([[5, 50]])
    expected_output = np.array([[0.1, -0.2]])

    output = scale_data(input_data)

    mock_joblib_load.assert_called_once_with('../../app/utils/feature_scalers/feature_scaler.joblib')
    mock_scaler.transform.assert_called_once_with(input_data)
    np.testing.assert_array_equal(output, expected_output)

    try:
        np.testing.assert_array_equal(output, expected_output)
        test_status = "PASSED"
    except AssertionError as e:
        test_status = f"FAILED: {str(e)}"

    with open("../../app/utils/performance/meta_scaler_test_results.txt", "a") as file:
        file.write(f"Test Status: {test_status}\n")
        file.write(f"Input Data:\n {input_data}\n")
        file.write(f"Expected Output:\n {expected_output}\n")
        file.write(f"Actual Output:\n {output}\n")
        file.write("-" * 50 + "\n")


@patch('app.utils.model.joblib.load')
def test_scale_data_large_input(mock_joblib_load):
    mock_scaler = MagicMock()
    mock_scaler.transform.return_value = np.random.rand(1000, 10)
    mock_joblib_load.return_value = mock_scaler

    input_data = np.random.rand(1000, 10)
    expected_output = mock_scaler.transform.return_value

    output = scale_data(input_data)

    mock_joblib_load.assert_called_once_with('../../app/utils/feature_scalers/feature_scaler.joblib')
    mock_scaler.transform.assert_called_once_with(input_data)
    np.testing.assert_array_equal(output, expected_output)

    try:
        np.testing.assert_array_equal(output, expected_output)
        test_status = "PASSED"
    except AssertionError as e:
        test_status = f"FAILED: {str(e)}"

    with open("../../app/utils/performance/meta_scaler_test_results.txt", "a") as file:
        file.write(f"Test Status: {test_status}\n")
        file.write(f"Input Data:\n {input_data}\n")
        file.write(f"Expected Output:\n {expected_output}\n")
        file.write(f"Actual Output:\n {output}\n")
        file.write("-" * 50 + "\n")


@patch('app.utils.model.joblib.load')
def test_scale_data_invalid_input(mock_joblib_load):
    mock_scaler = MagicMock()
    mock_scaler.transform.side_effect = ValueError("Invalid input data")
    mock_joblib_load.return_value = mock_scaler

    input_data = "invalid_input"

    with pytest.raises(ValueError):
        scale_data(input_data)

    mock_joblib_load.assert_called_once_with('../../app/utils/feature_scalers/feature_scaler.joblib')
    

@patch('app.utils.model.joblib.load')
def test_scale_data_different_shapes(mock_joblib_load):
    mock_scaler = MagicMock()
    mock_scaler.transform.return_value = np.array([[0.2, -0.3], [0.4, 0.5]])
    mock_joblib_load.return_value = mock_scaler

    input_data = np.array([[15, 150], [25, 250]])
    expected_output = np.array([[0.2, -0.3], [0.4, 0.5]])

    output = scale_data(input_data)

    mock_joblib_load.assert_called_once_with('../../app/utils/feature_scalers/feature_scaler.joblib')
    mock_scaler.transform.assert_called_once_with(input_data)
    np.testing.assert_array_equal(output, expected_output)

    try:
        np.testing.assert_array_equal(output, expected_output)
        test_status = "PASSED"
    except AssertionError as e:
        test_status = f"FAILED: {str(e)}"

    with open("../../app/utils/performance/meta_scaler_test_results.txt", "a") as file:
        file.write(f"Test Status: {test_status}\n")
        file.write(f"Input Data:\n {input_data}\n")
        file.write(f"Expected Output:\n {expected_output}\n")
        file.write(f"Actual Output:\n {output}\n")
        file.write("-" * 50 + "\n")

@patch('app.utils.model.joblib.load')
def test_scale_data_negative_values(mock_joblib_load):
    mock_scaler = MagicMock()
    mock_scaler.transform.return_value = np.array([[-0.5, -1.2], [-1.3, -0.7]])
    mock_joblib_load.return_value = mock_scaler

    input_data = np.array([[-10, -100], [-20, -200]])
    expected_output = np.array([[-0.5, -1.2], [-1.3, -0.7]])

    output = scale_data(input_data)

    mock_joblib_load.assert_called_once_with('../../app/utils/feature_scalers/feature_scaler.joblib')
    mock_scaler.transform.assert_called_once_with(input_data)
    np.testing.assert_array_equal(output, expected_output)

    try:
        np.testing.assert_array_equal(output, expected_output)
        test_status = "PASSED"
    except AssertionError as e:
        test_status = f"FAILED: {str(e)}"

    with open("../../app/utils/performance/meta_scaler_test_results.txt", "a") as file:
        file.write(f"Test Status: {test_status}\n")
        file.write(f"Input Data:\n {input_data}\n")
        file.write(f"Expected Output:\n {expected_output}\n")
        file.write(f"Actual Output:\n {output}\n")
        file.write("-" * 50 + "\n")

@patch('app.utils.model.joblib.load')
def test_scale_data_zeros(mock_joblib_load):
    mock_scaler = MagicMock()
    mock_scaler.transform.return_value = np.array([[0, 0], [0, 0]])
    mock_joblib_load.return_value = mock_scaler

    input_data = np.array([[0, 0], [0, 0]])
    expected_output = np.array([[0, 0], [0, 0]])

    output = scale_data(input_data)

    mock_joblib_load.assert_called_once_with('../../app/utils/feature_scalers/feature_scaler.joblib')
    mock_scaler.transform.assert_called_once_with(input_data)
    np.testing.assert_array_equal(output, expected_output)

    try:
        np.testing.assert_array_equal(output, expected_output)
        test_status = "PASSED"
    except AssertionError as e:
        test_status = f"FAILED: {str(e)}"

    with open("../../app/utils/performance/meta_scaler_test_results.txt", "a") as file:
        file.write(f"Test Status: {test_status}\n")
        file.write(f"Input Data:\n {input_data}\n")
        file.write(f"Expected Output:\n {expected_output}\n")
        file.write(f"Actual Output:\n {output}\n")
        file.write("-" * 50 + "\n")

@patch('app.utils.model.joblib.load')
def test_scale_data_high_values(mock_joblib_load):
    mock_scaler = MagicMock()
    mock_scaler.transform.return_value = np.array([[10, 20], [30, 40]])
    mock_joblib_load.return_value = mock_scaler

    input_data = np.array([[1000, 2000], [3000, 4000]])
    expected_output = np.array([[10, 20], [30, 40]])

    output = scale_data(input_data)

    mock_joblib_load.assert_called_once_with('../../app/utils/feature_scalers/feature_scaler.joblib')
    mock_scaler.transform.assert_called_once_with(input_data)
    np.testing.assert_array_equal(output, expected_output)

    try:
        np.testing.assert_array_equal(output, expected_output)
        test_status = "PASSED"
    except AssertionError as e:
        test_status = f"FAILED: {str(e)}"

    with open("../../app/utils/performance/meta_scaler_test_results.txt", "a") as file:
        file.write(f"Test Status: {test_status}\n")
        file.write(f"Input Data:\n {input_data}\n")
        file.write(f"Expected Output:\n {expected_output}\n")
        file.write(f"Actual Output:\n {output}\n")
        file.write("-" * 50 + "\n")

@patch('app.utils.model.joblib.load')
def test_scale_data_nan_values(mock_joblib_load):
    mock_scaler = MagicMock()
    mock_scaler.transform.return_value = np.array([[np.nan, np.nan], [np.nan, np.nan]])
    mock_joblib_load.return_value = mock_scaler

    input_data = np.array([[np.nan, np.nan], [np.nan, np.nan]])
    expected_output = np.array([[np.nan, np.nan], [np.nan, np.nan]])

    output = scale_data(input_data)

    mock_joblib_load.assert_called_once_with('../../app/utils/feature_scalers/feature_scaler.joblib')
    mock_scaler.transform.assert_called_once_with(input_data)
    np.testing.assert_array_equal(output, expected_output)

    mock_joblib_load.assert_called_once_with('../../app/utils/feature_scalers/feature_scaler.joblib')
    mock_scaler.transform.assert_called_once_with(input_data)
    try:
        np.testing.assert_array_equal(output, expected_output)
        test_status = "PASSED"
    except AssertionError as e:
        test_status = f"FAILED: {str(e)}"

    with open("../../app/utils/performance/meta_scaler_test_results.txt", "a") as file:
        file.write(f"Test Status: {test_status}\n")
        file.write(f"Input Data:\n {input_data}\n")
        file.write(f"Expected Output:\n {expected_output}\n")
        file.write(f"Actual Output:\n {output}\n")
        file.write("-" * 50 + "\n")
