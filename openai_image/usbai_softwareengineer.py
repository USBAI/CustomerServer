from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import openai

openai.api_key = "sk-proj-Q1JLGoe7A3rRoZaqyUh9T3BlbkFJv7YuuWTvZccPiUAyp9Ji"

global_history = []

@csrf_exempt
def handle_post_request(request):
    global global_history
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            history = data.get('history')
            if history:
                global_history = history  # Store the history data in the global variable
                print(f'Received history: {history}')
                return JsonResponse({'message': 'History data received.'})
            else:
                return JsonResponse({'error': 'No history data submitted.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def image_recognition(request):
    global global_history
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get("message", "")
            conversation_history = data.get("history", [])
            history_text = "\n".join([f"User: {entry['user']}\nBot: {entry['bot']}" for entry in conversation_history])

            prompt_tuning = f'''
                {message}
                About you=[
                    you are a software developer redy to assist users
                    you go by the name usbai or USB-AI an device that is Finetunend and prompt tuned 
                    to write computer programes to simplify the way we comput
                    you were developed in Sweden, Stockholm in 2024,
                    you were developed by Ernest Itangishaka
                ]

                User=[
                    Here is the user data when you find History=, then that mean that is the history of you and
                    the user convesetions and when you sind Prompt=, then that the 
                    user prompt is asking something then you can user the History to read and understand the previuse convesetion
                    so that you make a better and high quality output
                ]


                YouWork=[
                    you are a software engineer and you are here to assit humman to only things that
                    is related to code other wise let them know that you know the answer but im traind to 
                    respond to this questions but im glad to help you on things related to writing code or in the
                    fuild of softeare engineering
                ]

                Software Engineer=[
                    Here you are a software engineer

                    Attention[
                        if the user request is regarding on creating a software application 
                        Part[frontend, backend, fullstack, other...][
                            try to send some questions regarding about the software the user is looking for
                            remeber to try and get some few questions and if you find that the software is something
                            that can be frontend or backend then i need you to ask something like tools that will be used  
                        ]

                        History[
                            in the history we have our previous convesetion and once you have collacted all the tools and and
                            thing that will be use libraries and language the i need you to return this to the use
                            <the programming language here> <<the libraries here>> <<<the other tools that will be needed>>> and 
                            use this tags for each only is the user is ready to get started then return this
                        ]

                        Getting Started[
                             if it is front end return <frontend>place the whole full plane, from 0 to finish, 
                             this can be creating a folder then run this command then create this files but and for each file 
                             descrbe the code that will be in it but dont write the code just explain everything step by step
                             <frontend>

                             same with backend you can use <backend>Full steps<backend>
                        ]
                    ]
                ]
            '''

            def generate_chat_response(message):
                response = openai.ChatCompletion.create(
                    model="gpt-4-turbo",
                    messages=[
                        {"role": "system", "content": prompt_tuning},
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
