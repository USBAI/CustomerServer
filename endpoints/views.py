from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import openai
import time
from requests.exceptions import HTTPError

openai.api_key = "sk-proj-Q1JLGoe7A3rRoZaqyUh9T3BlbkFJv7YuuWTvZccPiUAyp9Ji"

# Prompt for GPT-3
def create_chat_completion(question):
    retries = 3
    for i in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a Genius!"},
                    {"role": "user", "content": question},
                ]
            )
            output_text = response["choices"][0]["message"]["content"]
            print("Generated response:", output_text)  # Print generated response
            return output_text
        except HTTPError as e:
            if e.response.status_code == 429:  # Rate limit exceeded
                wait_time = (2 ** i) * 0.5  # Exponential backoff
                print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise  # Re-raise other HTTP errors

@csrf_exempt
def handle_request(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Received request data:", data)

            question = data.get('question')  # Extract question from data

            if question:
                response_text = create_chat_completion(question)
                return JsonResponse({'message': response_text})
            else:
                return JsonResponse({'error': 'Missing "question" field in request data'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in request'}, status=400)
        except Exception as e:
            print(f"An error occurred: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
