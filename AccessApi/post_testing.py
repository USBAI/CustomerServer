import requests
import json

BASE_URL = "http://127.0.0.1:8000/AccessApi"

# Data for registration for two accounts
accounts = [
    {
        "company_name": "Kluret",
        "email": "test@kluret.com",
        "website_url": "https://kluretab.com",
        "plan": "Professional",
        "password": "securepassword",
        "confirm_password": "securepassword"
    }
]

# Loop through each account to register, login, and fetch user information
for account in accounts:
    # Step 1: Register a new user
    print(f"Registering a new user for {account['company_name']}...")
    register_response = requests.post(f"{BASE_URL}/register/", json=account)

    if register_response.status_code == 200:
        register_result = register_response.json()
        print("Registration Successful:", json.dumps(register_result, indent=4))
        api_key = register_result['api_key']
        user_uuid = register_result['user_uuid']
    else:
        print("Registration Failed:", register_response.text)
        continue  # Skip to the next account

    # Data for login
    login_data = {
        "email": account["email"],
        "password": account["password"]
    }

    # Step 2: Login with the registered user
    print(f"\nLogging in for {account['company_name']}...")
    login_response = requests.post(f"{BASE_URL}/login/", json=login_data)

    if login_response.status_code == 200:
        login_result = login_response.json()
        print("Login Successful:", json.dumps(login_result, indent=4))
        token = login_result['token']
    else:
        print("Login Failed:", login_response.text)
        continue  # Skip to the next account

    # Data for getting user information
    get_user_info_data = {
        "user_uuid": user_uuid
    }

    # Step 3: Get user information
    print(f"\nFetching user information for {account['company_name']}...")
    get_user_info_response = requests.post(f"{BASE_URL}/get_user_info/", json=get_user_info_data)

    if get_user_info_response.status_code == 200:
        user_info = get_user_info_response.json()
        print("User Information Retrieved Successfully:", json.dumps(user_info, indent=4))
    else:
        print("Failed to Retrieve User Information:", get_user_info_response.text)
