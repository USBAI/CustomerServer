import requests

# Define the API endpoint
url = "http://127.0.0.1:8004/users_order/add-user-order/"

# Define the data to be sent in the POST request
data = {
    "post_value": "xpn"  # Replace with the appropriate key-value pair as needed
}

# Send the POST request to the API
response = requests.post(url, json=data)

# Print the status code and the response data
print(f"Status Code: {response.status_code}")
print("Response Data:", response.json())
