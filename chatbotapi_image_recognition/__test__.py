import requests
import json

# Define the API endpoint
url = "http://localhost:8000/chatbotapi_image_recognition/chatbot/"

# Define the request payload
payload = {
    "user_input": "Describe this product",
    "user_history": "",
    "user_id": "test_user_123",  # Replace with an actual user ID if needed
    "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjTA81d-wVUh3nKiMAj2BUqJeqG9_k0N30uA&s"
}

# Define the headers
headers = {
    "Content-Type": "application/json"
}

# Send the POST request
try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Print the response
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())

except Exception as e:
    print("An error occurred:", e)
