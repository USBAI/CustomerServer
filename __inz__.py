import hashlib
import os
import pyautogui
import requests
import json
import random
import string
from flask import Flask, request, jsonify, render_template_string
import threading
import logging
import webbrowser  # Import webbrowser module for opening the browser

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)  # Changed from CRITICAL to DEBUG

HTML_TEMPLATE = """
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
            height: calc(100vh - 50px);
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
        .leftdiv__234j9 {
            margin-top: 5px;
        }
        #chat-container {
            flex: 1;
            overflow-y: auto;
            display: flex;
            flex-direction: column-reverse;
            padding: 10px;
            margin-top: 50px;
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
                typeSlowly(data.response, 'bot-message', true);
            })
            .catch(error => {
                const chatContainer = document.getElementById('chat-container');
                chatContainer.removeChild(loadingDiv);
                addMessage('Error occurred. Please try again.', 'bot-message');
            });
        }

        function addMessage(text, className, isHTML = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${className}`;
            if (isHTML) {
                messageDiv.innerHTML = text;
            } else {
                messageDiv.textContent = text;
            }
            addMessageElement(messageDiv);
        }

        function addMessageElement(element) {
            const chatContainer = document.getElementById('chat-container');
            chatContainer.insertBefore(element, chatContainer.firstChild);
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
                }
            }
            typeNextCharacter();
        }
    </script>
</body>
</html>
"""

# Function to generate a random filename
def generate_random_filename(length_range=(30, 60)):
    length = random.randint(*length_range)
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return random_str + '.json'

# Function to save conversation to JSON file
def save_conversation_to_json(filepath, user_input, response_text):
    data = {
        'user': user_input,
        'bot': response_text
    }
    with open(filepath, 'a') as json_file:
        json.dump(data, json_file)
        json_file.write('\n')

# Function to upload image
def upload_image(image_path):
    url = 'https://neurodrive-client-21a811329970.herokuapp.com/api/upload/'
    files = {'image': open(image_path, 'rb')}
    response = requests.post(url, files=files, verify=False)
    return response

# Function to post JSON data to Django API
def post_json_data_to_django_api(json_filepath):
    url = 'http://neurodrive-client-21a811329970.herokuapp.com/openai_image/handle_post/'
    with open(json_filepath, 'r') as json_file:
        for line in json_file:
            data = json.loads(line)
            history = json.dumps(data)
            response = requests.post(url, data={'history': history})

# Flask route for the main page
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

# Flask route to handle user input
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

        try:
            response = upload_image(file_path)
            os.remove(file_path)

            url = 'https://neurodrive-client-21a811329970.herokuapp.com/image_recognition/imagerecognition/'
            message = f"https://neurodrive-client-21a811329970.herokuapp.com/media/images/{hashed_filename}"
            data = {"message": message}

            response = requests.post(url, json=data, verify=False)

            if response.status_code == 200:
                response_text = response.json().get('response', '')
            else:
                response_text = "Error: " + response.text

            save_conversation_to_json(current_json_filepath, user_input, response_text)
            post_json_data_to_django_api(current_json_filepath)

            return jsonify({'response': response_text})
        except Exception as e:
            return jsonify({'response': f"Error occurred: {str(e)}"}), 500

    return jsonify({'response': 'No input received'}), 400

# Function to open the web browser to display Flask app
def open_browser():
    webbrowser.open('http://localhost:5000')

# Main entry point
if __name__ == '__main__':
    # Create data directory if it doesn't exist
    if not os.path.exists("D:\\data"):
        os.makedirs("D:\\data")

    # Generate a random JSON file path
    current_json_filepath = os.path.join("D:\\data", generate_random_filename())

    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=app.run, kwargs={'debug': True})
    flask_thread.daemon = True
    flask_thread.start()

    # Open the default web browser after a short delay to ensure Flask app has started
    threading.Timer(2, open_browser).start()
