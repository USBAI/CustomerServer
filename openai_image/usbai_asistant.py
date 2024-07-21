from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import openai

openai.api_key = "sk-proj-Q1JLGoe7A3rRoZaqyUh9T3BlbkFJv7YuuWTvZccPiUAyp9Ji"



global_history = ""

@csrf_exempt
def handle_post_request(request):
    global global_history
    if request.method == 'POST':
        history = request.POST.get('history')
        if history:
            global_history = history  # Store the history data in the global variable
            print(f'Received history: {history}')
            return JsonResponse({'message': 'Hello'})
        else:
            return JsonResponse({'error': 'No history data submitted.'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def image_recognition(request):
    global global_history
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get("message", "")

            prompt_tuning = f'''
            you are now a prompt tuned model so act like that 

            --- 
            you are a software developer you are allowed to communicate with users so do your job and you name is Alex

            me and you we are talking so here is our history chat! dont look at the image just ignor it till if you detect that the
            image is needed then you we can talk about the image but only if the user asks you to from this data: 
            
            
            this is a chat history so i need you to sound like a real human and act like you are to king with someone and you can 
            remember the past so this is the past data and if the user start talking about the past so you know this it the
            history data but dont tell the user this is the past json data just sound like a real human{global_history}
            '''

            def generate_chat_response(image_url):
                response = openai.ChatCompletion.create(
                    model="gpt-4-turbo",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt_tuning},
                                {"type": "image_url", "image_url": {"url": image_url}}
                            ]
                        }
                    ],
                    max_tokens=300
                )
                return response.choices[0].message.content

            response_content = generate_chat_response(message)
            response_data = {"response": response_content}

            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    else:
        return JsonResponse({"error": "Method Not Allowed"}, status=405)