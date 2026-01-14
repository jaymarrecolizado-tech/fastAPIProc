"""
Quick test to verify CORS is working
Run this to test CORS headers
"""
import requests

# Test CORS preflight
response = requests.options(
    'http://localhost:8000/api/v1/auth/login',
    headers={
        'Origin': 'http://localhost:3000',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'Content-Type'
    }
)

print("CORS Preflight Test:")
print(f"Status: {response.status_code}")
print(f"Headers:")
for key, value in response.headers.items():
    if 'access-control' in key.lower():
        print(f"  {key}: {value}")

if 'Access-Control-Allow-Origin' in response.headers:
    print("\n✅ CORS is configured correctly!")
else:
    print("\n❌ CORS headers missing!")
