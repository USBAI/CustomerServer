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
            Here is our history so read this first and understand the user history to be able to respond to the user request so here is the reques
             history=[{global_history}]
            Just read the bottom question which is userr and read it after understanding the question read the history
            [{global_history}] then after you have got he response and if it about the screen then take the infromation from the 
            screen then respnond as a real lift vision assistant like dont say based on the image just use word like see this on you computer screen
            meaning i neeed you to act like a screen reader but the user shall not know that it is a screenshort!

            and i need you to be helpfull and pay attention to you response based on the letest question given in the history and the 
            user might ask things based on your previouse response so i need you to act like you remember everything and the responsse 
            shall be like a humment talking to other humman!
            
            '''

            def generate_chat_response(image_url):
                response = openai.ChatCompletion.create(
                    model="gpt-4-turbo",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": f"{prompt_tuning}"},
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