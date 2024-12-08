import requests
import json

# API URL
url = "http://127.0.0.1:8000/ConnectStoreAuth/register/"

# Sample data to send in the POST request
payload = {
    "store_name": "Test Store",
    "email": "test@test.com",
    "website_url": "https://test.com",
    "store_type": "Shopify",
    "password": "1234",
    "confirm_password": "1234"
}

# Headers for the request
headers = {
    "Content-Type": "application/json"
}

# Make the POST request to the API
try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    # Print the response
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
except Exception as e:
    print("An error occurred:", str(e))
