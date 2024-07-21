import openai

# Set your OpenAI API key
openai.api_key = "sk-proj-Q1JLGoe7A3rRoZaqyUh9T3BlbkFJv7YuuWTvZccPiUAyp9Ji"

# User input (replace with input() for terminal input)
user_input = input("Chat: ")

# Create the completion using GPT-3.5 Turbo
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a Genius!"},
        {"role": "user", "content": user_input},
    ]
)

# Extract output text from response
output_text = response["choices"][0]["message"]["content"]

# Print the response
print("Response from GPT-3.5 Turbo:")
print(output_text)
