import requests
import json

# API URL
url = "https://customerserver1-5d81976997ba.herokuapp.com/ConnectStoreServer/get_store_info/"

# Sample data to send in the POST request
payload = {
    'store_id': '2e989170-56a9-454b-87f6-fee5a0a130ae',
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
