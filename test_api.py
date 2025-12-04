import requests
import json
import time

API_BASE = "http://localhost:5000"

print("Testing RAG System API...")
print("=" * 50)

time.sleep(2)

print("\n1. Testing Health Endpoint...")
try:
    response = requests.get(f"{API_BASE}/api/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

print("\n2. Testing Stats Endpoint...")
try:
    response = requests.get(f"{API_BASE}/api/stats")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

print("\n3. Testing Query Endpoint...")
try:
    test_query = {
        "query": "What is RAG?",
        "use_transformation": True
    }
    response = requests.post(
        f"{API_BASE}/api/query",
        json=test_query,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"\nAnswer: {result.get('answer', 'N/A')[:200]}...")
    print(f"\nSources: {len(result.get('sources', []))} chunks retrieved")
    if result.get('sources'):
        for i, source in enumerate(result.get('sources', [])[:3], 1):
            print(f"  {i}. {source.get('filename')} - Similarity: {source.get('similarity', 0):.2%}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 50)
print("Testing complete!")

