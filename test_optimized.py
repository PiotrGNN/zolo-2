import requests
import time

start = time.time()
response = requests.get('http://localhost:5001/api/portfolio', timeout=10)
elapsed = time.time() - start

print(f'Time: {elapsed:.2f}s')
print(f'Status: {response.status_code}')
data = response.json()
print(f'Data source: {data.get("data_source", "unknown")}')
print(f'Balance: {data.get("total_value", "N/A")}')
print(f'Environment: {data.get("environment", "unknown")}')
