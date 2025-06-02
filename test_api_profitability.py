import requests
import numpy as np

def test_api_profitability():
    X = np.random.randn(100, 3).tolist()
    y = (np.cumsum(np.random.randn(100)) + 100).tolist()

    payload = {
        "X": X,
        "y": y
    }

    url = "http://127.0.0.1:5000/api/models/profitability"
    response = requests.post(url, json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "profitability" in data or "metrics" in data
