from django.http import JsonResponse
import json

data = '''
import hashlib
import os
import pyautogui
import requests
import json
import random
import string
from flask import Flask, request, jsonify, render_template_string
import webview
import threading
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)  # Changed from CRITICAL to DEBUG

HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>USB-AI</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        body {
            display: flex;
            flex-direction: column;
            height: calc(100vh - 50px); /* Adjusted for bottom bar */
            background-color: #fae6ff;
            margin: 0;
        }
        #navbar {
            position: fixed;
            width: 100%;
            background-color: #fae6ff00;
            backdrop-filter: blur(5px);
            color: black;
            padding: 10px;
            z-index: 1000;
            display: flex;
            justify-content: space-between;
            box-shadow: 2px 2px 20px 2px #007bff12;
        }
        .leftdiv__234j9{
            margin-top: 5px;
        }
        #chat-container {
            flex: 1;
            overflow-y: auto;
            display: flex;
            flex-direction: column-reverse;
            padding: 10px;
            margin-top: 50px; /* Adjusted for navbar height */
        }
        .message {
            max-width: 80%;
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 5px;
            position: relative;
        }
        .user-message {
            align-self: flex-end;
            background-color: #DCF8C6;
        }
        .bot-message {
            align-self: flex-start;
            background-color: #E8E8E8;
        }
        .copy-icon {
            position: absolute;
            right: -25px;
            top: 50%;
            transform: translateY(-50%);
            cursor: pointer;
            color: #007BFF;
        }
        #input-container {
            display: flex;
            padding: 10px;
            border-top: 1px solid #ccc;
        }
        #input-container input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        #input-container button {
            margin-left: 10px;
            padding: 10px 20px;
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 5px;
        }
        .loading {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .loading div {
            width: 8px;
            height: 8px;
            margin: 0 4px;
            background-color: #007BFF;
            border-radius: 50%;
            animation: bounce 1.4s infinite ease-in-out both;
        }
        .loading div:nth-child(1) {
            animation-delay: -0.32s;
        }
        .loading div:nth-child(2) {
            animation-delay: -0.16s;
        }
        @keyframes bounce {
            0%, 80%, 100% {
                transform: scale(0);
            }
            40% {
                transform: scale(1);
            }
        }
    </style>
</head>
<body>
    <div id="navbar">
        <div class="logo">
            <svg width="30" height="30" viewBox="0 0 122 122" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="122" height="122" rx="61" fill="black"/>
                <rect x="48" y="16" width="64" height="64" rx="32" fill="white"/>
                <path d="M2 77H120C120 82.5228 115.523 87 110 87H12C6.47715 87 2 82.5228 2 77Z" fill="white"/>
            </svg>
        </div>
        <div class="leftdiv__234j9">
            <a href="https://www.usbai.org" target="_blank">Help?</a>
        </div>
    </div>
    <div id="chat-container"></div>
    <div id="input-container">
        <input type="text" id="question" placeholder="Type your message here..." onkeypress="handleKeyPress(event)">
        <button onclick="sendMessage()">Send</button>
    </div>
    <script>
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        function sendMessage() {
            const questionInput = document.getElementById('question');
            const question = questionInput.value;
            if (!question) return;

            addMessage(question, 'user-message');
            questionInput.value = '';

            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'message bot-message loading';
            loadingDiv.innerHTML = '<div></div><div></div><div></div><div></div>';
            addMessageElement(loadingDiv);

            fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question }),
            })
            .then(response => response.json())
            .then(data => {
                const chatContainer = document.getElementById('chat-container');
                chatContainer.removeChild(loadingDiv);
                const formattedResponse = formatResponse(data.response);
                typeSlowly(formattedResponse, 'bot-message', true);
            })
            .catch(error => {
                const chatContainer = document.getElementById('chat-container');
                chatContainer.removeChild(loadingDiv);
                addMessage('Error occurred. Please try again.', 'bot-message');
            });
        }

        function formatResponse(text) {
            return text.replace(/\*\*(.*?)\*\*/g, '<h1>$1</h1>');
        }

        function addMessage(text, className, isHTML = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${className}`;
            if (isHTML) {
                messageDiv.innerHTML = text;
            } else {
                messageDiv.textContent = text;
            }

            if (className === 'bot-message' && !isHTML) {
                const copyIcon = document.createElement('span');
                copyIcon.className = 'copy-icon';
                copyIcon.textContent = '📋';
                copyIcon.onclick = () => copyToClipboard(text);
                messageDiv.appendChild(copyIcon);
            }

            addMessageElement(messageDiv);
        }

        function addMessageElement(element) {
            const chatContainer = document.getElementById('chat-container');
            chatContainer.insertBefore(element, chatContainer.firstChild);
        }

        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                alert('Copied to clipboard');
            }, (err) => {
                console.error('Error copying text: ', err);
            });
        }

        function typeSlowly(text, className, isHTML = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${className}`;
            addMessageElement(messageDiv);

            let i = 0;
            function typeNextCharacter() {
                if (i < text.length) {
                    if (isHTML) {
                        messageDiv.innerHTML += text.charAt(i);
                    } else {
                        messageDiv.textContent += text.charAt(i);
                    }
                    i++;
                    setTimeout(typeNextCharacter, 20); // Adjust the typing speed here
                } else {
                    const copyIcon = document.createElement('span');
                    copyIcon.className = 'copy-icon';
                    copyIcon.textContent = '📋';
                    copyIcon.onclick = () => copyToClipboard(text);
                    messageDiv.appendChild(copyIcon);
                }
            }
            typeNextCharacter();
        }
    </script>
</body>
</html>
"""

def generate_random_filename(length_range=(30, 60)):
    length = random.randint(*length_range)
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return random_str + '.json'

def save_conversation_to_json(filepath, user_input, response_text):
    data = {
        'user': user_input,
        'bot': response_text
    }
    with open(filepath, 'a') as json_file:
        json.dump(data, json_file)
        thebak_n='n'
        json_file.write(f'\{thebak_n}')

def upload_image(image_path):
    url = 'https://neurodrive-client-21a811329970.herokuapp.com/api/upload/'
    files = {'image': open(image_path, 'rb')}
    response = requests.post(url, files=files)
    return response

def post_json_data_to_django_api(json_filepath):
    url = 'http://neurodrive-client-21a811329970.herokuapp.com/openai_image/handle_post/'
    with open(json_filepath, 'r') as json_file:
        for line in json_file:
            data = json.loads(line)
            history = json.dumps(data)
            response = requests.post(url, data={'history': history})

@app.route('/')
def index():
    return "Flask server is running"

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('question')
    if user_input:
        screenshot = pyautogui.screenshot()
        
        hash_object = hashlib.sha1(user_input.encode())
        hashed_filename = hash_object.hexdigest()[:30] + '.png'
        directory = "usbai.vision"
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = os.path.join(directory, hashed_filename)
        screenshot.save(file_path)

        response = upload_image(file_path)
        
        os.remove(file_path)

        url = 'https://neurodrive-client-21a811329970.herokuapp.com/image_recognition/imagerecognition/'

        message = f"https://neurodrive-client-21a811329970.herokuapp.com/media/images/{hashed_filename}"

        data = {
            "message": message
        }

        response = requests.post(url, json=data)

        if response.status_code == 200:
            response_text = response.json().get('response', '')
        else:
            response_text = "Error: " + response.text

        # Detect if response is HTML
        if response_text.startswith("```html") and response_text.endswith("```"):
            response_text = response_text[7:-3].strip()

        response_text = response_text.replace('**', '<h1>').replace('<h1>', '</h1>', 1).replace('</h1>', '<h1>', 1)

        save_conversation_to_json(current_json_filepath, user_input, response_text)
        post_json_data_to_django_api(current_json_filepath)

        return jsonify({'response': response_text})
    return jsonify({'response': 'No question provided'}), 400

def start_flask_app():
    app.run(debug=True, port=5000, use_reloader=False)

if __name__ == '__main__':
    if not os.path.exists("D:\\data"):
        os.makedirs("D:\\data")

    current_json_filepath = os.path.join("D:\\data", generate_random_filename())

    flask_thread = threading.Thread(target=start_flask_app)
    flask_thread.daemon = True
    flask_thread.start()

    # Disable fullscreen and set position
    window = webview.create_window("USB-AI", "http://localhost:5000", width=500, height=820, min_size=(300, 800), fullscreen=False)
    webview.start()
'''

def usbai_django_get(request):
    if request.method == 'GET':
        response_data = {
            "code": data.strip()
        }
        return JsonResponse(response_data, json_dumps_params={'indent': 2})
