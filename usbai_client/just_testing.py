import requests

# Base URL of your Django application
BASE_URL = "http://127.0.0.1:8000"  # Replace with your Django server's URL

# Endpoints to test
endpoints = [
    "/",  # Root
    "/admin/",
    "/client/",
    "/api/",
    "/usbai_vision/",
]

# Test cases
headers_with_valid_key = {"X-API-KEY": "eiojwhd93reugh9euf0ehdovivfkcjgfheodfoeoigjeuffhuhooh"}
headers_with_invalid_key = {"X-API-KEY": "invalid_key"}
headers_without_key = {}

print("Testing API key validation...\n")

for endpoint in endpoints:
    print(f"Testing endpoint: {endpoint}")
    
    # Test with valid API key
    response = requests.get(BASE_URL + endpoint, headers=headers_with_valid_key)
    print(f"  Valid Key - Status Code: {response.status_code}, URL: {response.url}")
    
    # Test with invalid API key
    response = requests.get(BASE_URL + endpoint, headers=headers_with_invalid_key)
    print(f"  Invalid Key - Status Code: {response.status_code}, URL: {response.url}")
    
    # Test without API key
    response = requests.get(BASE_URL + endpoint, headers=headers_without_key)
    print(f"  No Key - Status Code: {response.status_code}, URL: {response.url}")

print("\nTesting completed.")
