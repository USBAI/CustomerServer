import openai

openai.api_key = "sk-proj-Q1JLGoe7A3rRoZaqyUh9T3BlbkFJv7YuuWTvZccPiUAyp9Ji"

def generate_chat_response(image_url):
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "explain things in details what you see and list them"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ],
        max_tokens=300
    )
    return response.choices[0]

if __name__ == "__main__":
    image_path = "https://neurodrive-client-21a811329970.herokuapp.com/media/images/screenshot.png"
    response = generate_chat_response(image_path)
    print(response.message.content)





#________________________________________________________________________





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

            # First GPT-4 call for text analysis
            prompt_tuning_text = f'''
            Based on the following conversation history:
            "{global_history}"

            The user just sent this message: "{message}".

            Please determine if this message requires generating or analyzing an image. 
            If the user is requesting an image or asking about something visible on their screen, respond only with "<true><true>". 
            If the user's message does not require generating or analyzing an image, respond only with "<false>{{message to communicate to the user}}<false>". 
            '''

            response_text_analysis = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": prompt_tuning_text
                    }
                ],
                max_tokens=100
            )

            text_analysis_content = response_text_analysis.choices[0].message['content']

            # Check the response from text analysis
            if "<true><true>" in text_analysis_content:
                # Proceed with image generation
                prompt_tuning_image = f'''
                We have a conversation history as follows: {global_history}.
                Based on the user's latest message, they require image processing. 
                Please generate the appropriate image response for the following message: "{message}".
                '''

                def generate_chat_response(image_url):
                    response = openai.ChatCompletion.create(
                        model="gpt-4-turbo",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": prompt_tuning_image},
                                    {"type": "image_url", "image_url": {"url": image_url}}
                                ]
                            }
                        ],
                        max_tokens=300
                    )
                    return response.choices[0].message['content']

                response_content = generate_chat_response(message)
                response_data = {"response": response_content}
                return JsonResponse(response_data)
            
            elif "<false>" in text_analysis_content:
                # Extract the message between <false>{content}<false> tags
                start_index = text_analysis_content.find("<false>") + 7
                end_index = text_analysis_content.find("<false>", start_index)
                user_message = text_analysis_content[start_index:end_index].strip()

                response_data = {"response": user_message}
                return JsonResponse(response_data)
            else:
                return JsonResponse({"error": "Unexpected response format from text analysis."}, status=500)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    else:
        return JsonResponse({"error": "Method Not Allowed"}, status=405)
