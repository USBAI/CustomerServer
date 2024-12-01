import httpx

url = "https://customerserver1-5d81976997ba.herokuapp.com/users/register_user"
payload = {"email": "testuser@example.com", "password": "securepassword123"}
headers = {"Content-Type": "application/json"}

response = httpx.post(url, json=payload, headers=headers, timeout=30)
print(response.status_code)
print(response.json())
