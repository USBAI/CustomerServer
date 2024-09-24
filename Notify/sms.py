from twilio.rest import Client

# Your Twilio account SID and Auth Token from twilio.com/console
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'

client = Client(account_sid, auth_token)

# Send the SMS
message = client.messages.create(
    body="Hello! This is a test message from Twilio.",  # The message body
    from_='+1234567890',  # Your Twilio phone number
    to='+46727759188'  # The recipient phone number
)

print(f"Message sent with SID: {message.sid}")
