import pytest
import httpx
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"

test_data = [
    {"endpoint": "/sum", "data": {"a": 5, "b": 3}, "expected": 8},
    {"endpoint": "/subtract", "data": {"a": 5, "b": 3}, "expected": 2},
    {"endpoint": "/multiply", "data": {"a": 5, "b": 3}, "expected": 15},
    {"endpoint": "/divide", "data": {"a": 6, "b": 3}, "expected": 2},
    {"endpoint": "/divide", "data": {"a": 5, "b": 0}, "expected": "Division by zero is not allowed"},
]

@pytest.mark.parametrize("test_case", test_data)
def test_api_endpoints(test_case):
    endpoint = test_case["endpoint"]
    data = test_case["data"]
    expected = test_case["expected"]

    response = httpx.post(BASE_URL + endpoint, json=data)
    response_data = response.json()

    if "error" in response_data:
        result = response_data["error"]
    else:
        result = response_data["result"]

    assert result == expected

def save_results_to_csv(results):
    df = pd.DataFrame(results)
    df.to_csv("test_results.csv", index=False)

def test_api_and_save_results():
    results = []

    for test_case in test_data:
        endpoint = test_case["endpoint"]
        data = test_case["data"]
        expected = test_case["expected"]

        response = httpx.post(BASE_URL + endpoint, json=data)
        response_data = response.json()

        if "error" in response_data:
            result = response_data["error"]
        else:
            result = response_data["result"]

        success = result == expected
        results.append({
            "endpoint": endpoint,
            "data": data,
            "expected": expected,
            "result": result,
            "success": success
        })

    save_results_to_csv(results)

if __name__ == "__main__":
    pytest.main(["-v", "--tb=short", "-s", __file__])
    test_api_and_save_results()
