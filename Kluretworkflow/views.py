import os
import firebase_admin
from firebase_admin import credentials, db
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Path to Firebase credentials JSON file for the first Firebase Realtime Database
FIREBASE_CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), 'firebase_credentials.json')

# Initialize Firebase Admin SDK for the first Realtime Database
try:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://users-95da3-default-rtdb.europe-west1.firebasedatabase.app/',
        'storageBucket': 'users-95da3.appspot.com'  # Replace with your actual Firebase Storage bucket
    })
except FileNotFoundError as e:
    print(f"Firebase credentials file not found: {e}")
except Exception as e:
    print(f"Error initializing Firebase Admin SDK: {str(e)}")

# Path to Firebase credentials JSON file for the second Firebase Realtime Database
FIREBASE_CREDENTIALS_FOR_TASK_PATH = os.path.join(os.path.dirname(__file__), 'bolagdb-c40e2-firebase-adminsdk-y8rnh-3905b9b493.json')

# Initialize Firebase Admin SDK for the second Realtime Database
try:
    cred_task = credentials.Certificate(FIREBASE_CREDENTIALS_FOR_TASK_PATH)
    firebase_admin.initialize_app(cred_task, {
        'databaseURL': 'https://bolagdb-c40e2-default-rtdb.europe-west1.firebasedatabase.app/',
        'storageBucket': 'bolagdb-c40e2.appspot.com'  # Replace with the actual bucket name if necessary
    }, name='bolagdb')
except FileNotFoundError as e:
    print(f"Firebase credentials file for tasks not found: {e}")
except Exception as e:
    print(f"Error initializing Firebase Admin SDK for tasks: {str(e)}")


@csrf_exempt
def get_all_user_names(request):
    if request.method == 'GET':
        try:
            # Get a reference to the Firebase Realtime Database for the first database
            ref = db.reference('All_Users/Kluret_Users')

            # Get all users' data
            all_users = ref.get()

            if all_users:
                # Extract all the emails (usernames)
                usernames = [email.replace('dot', '.').replace('at', '@') for email in all_users.keys()]
                return JsonResponse({"status": "success", "usernames": usernames})
            else:
                return JsonResponse({"status": "failed", "message": "No users found"})

        except Exception as e:
            return JsonResponse({"status": "failed", "message": str(e)})

    return JsonResponse({"status": "failed", "message": "Only GET requests are allowed for fetching user names"})

@csrf_exempt
def get_all_chats(request):
    if request.method == 'GET':
        try:
            # Get a reference to the Firebase Realtime Database for the first database
            app = firebase_admin.get_app('bolagdb')
            ref = db.reference('Bolag_Kluret/Chat_History', app=app)

            # Get all users' data
            all_users = ref.get()

            # Count the total number of chat blocks
            total_chats = len(all_users) if all_users else 0

            if all_users:
                # Convert any sets in the all_users dictionary to lists
                all_users_serializable = {}
                for key, value in all_users.items():
                    if isinstance(value, set):
                        all_users_serializable[key] = list(value)  # Convert set to list
                    elif isinstance(value, dict):  # If value is a dictionary, ensure all sets are converted
                        all_users_serializable[key] = {k: list(v) if isinstance(v, set) else v for k, v in value.items()}
                    else:
                        all_users_serializable[key] = value  # Keep value as is

                return JsonResponse({"status": "success", "id": all_users_serializable, "total_chats": total_chats})
            else:
                return JsonResponse({"status": "failed", "message": "chat history not found", "total_chats": total_chats})

        except Exception as e:
            return JsonResponse({"status": "failed", "message": str(e), "total_chats": 0})

    return JsonResponse({"status": "failed", "message": "Only GET requests are allowed for fetching user names"})



# New function to retrieve tasks from the second Firebase Realtime Database using FIREBASE_CREDENTIALS_FOR_TASK_PATH
@csrf_exempt
def get_tasks_from_storage(request):
    if request.method == 'GET':
        try:
            # Get reference to the second Firebase app 'bolagdb' initialized with FIREBASE_CREDENTIALS_FOR_TASK_PATH
            app = firebase_admin.get_app('bolagdb')

            # Get a reference to the Firebase Realtime Database for the second database
            ref = db.reference('Bolag_Kluret/Tasks ', app=app)

            # Fetch all tasks
            tasks = ref.get()

            if tasks:
                # Format tasks data into a list
                task_list = []
                for task_key, task_value in tasks.items():
                    task_list.append({
                        "id": task_key,
                        "Date": task_value.get("Date"),
                        "Description": task_value.get("Description"),
                        "Topic": task_value.get("Topic"),
                        "Assigned_To": task_value.get("Assigned_To")
                    })

                return JsonResponse({"status": "success", "tasks": task_list})

            else:
                return JsonResponse({"status": "failed", "message": "No tasks found"})

        except Exception as e:
            return JsonResponse({"status": "failed", "message": str(e)})

    return JsonResponse({"status": "failed", "message": "Only GET requests are allowed for fetching tasks from storage"})
