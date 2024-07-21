import os
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

def zalando(request):
    # Paths to the JSON files
    file_path1 = os.path.join(settings.BASE_DIR, 'kluret_engine/web/zalando/pipline1/pipline1.json')
    file_path2 = os.path.join(settings.BASE_DIR, 'kluret_engine/web/zalando/pipline1/pipline2.json')
    file_path3 = os.path.join(settings.BASE_DIR, 'kluret_engine/web/zalando/pipline1/pipline3.json')
    file_path4 = os.path.join(settings.BASE_DIR, 'kluret_engine/web/zalando/pipline1/pipline4.json')
    file_path5 = os.path.join(settings.BASE_DIR, 'kluret_engine/web/zalando/pipline1/pipline5.json')
    file_path6 = os.path.join(settings.BASE_DIR, 'kluret_engine/web/zalando/pipline1/pipline6.json')
    file_path7 = os.path.join(settings.BASE_DIR, 'kluret_engine/web/zalando/pipline1/pipline7.json')
    file_path8 = os.path.join(settings.BASE_DIR, 'kluret_engine/web/zalando/pipline1/pipline8.json')
    
    try:
        with open(file_path1, 'r') as file1:
            product_details1 = json.load(file1)
    except FileNotFoundError:
        product_details1 = []

    try:
        with open(file_path2, 'r') as file2:
            product_details2 = json.load(file2)
    except FileNotFoundError:
        product_details2 = []

    try:
        with open(file_path3, 'r') as file3:
            product_details3 = json.load(file3)
    except FileNotFoundError:
        product_details3 = []

    try:
        with open(file_path4, 'r') as file4:
            product_details4 = json.load(file4)
    except FileNotFoundError:
        product_details4 = []

    try:
        with open(file_path5, 'r') as file5:
            product_details5 = json.load(file5)
    except FileNotFoundError:
        product_details5 = []


    try:
        with open(file_path6, 'r') as file6:
            product_details6 = json.load(file6)
    except FileNotFoundError:
        product_details6 = []


    try:
        with open(file_path7, 'r') as file7:
            product_details7 = json.load(file7)
    except FileNotFoundError:
        product_details7 = []


    try:
        with open(file_path8, 'r') as file8:
            product_details8 = json.load(file8)
    except FileNotFoundError:
        product_details8 = []

    
    
    # Combine the contents of both JSON files
    combined_product_details = product_details1 + product_details2 + product_details3 + product_details4 + product_details5  + product_details6 
    # + product_details7 + product_details8

    return JsonResponse(combined_product_details, safe=False)







@csrf_exempt
def update_pipeline(request):
    if request.method == 'POST':
        try:
            # Load JSON data from request body
            received_data = json.loads(request.body.decode('utf-8'))

            # File path to pipeline.json
            file_path = os.path.join(settings.BASE_DIR, 'kluret_engine/web/zalando/api/pipeline.json')

            # Load existing data from pipeline.json or create empty list
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    existing_data = json.load(file)
            else:
                existing_data = []

            # Append received_data to existing_data (assuming received_data is a list of products)
            existing_data.extend(received_data)

            # Write updated data back to pipeline.json
            with open(file_path, 'w') as file:
                json.dump(existing_data, file, indent=2)

            # Return updated data as JSON response
            return JsonResponse(existing_data, safe=False)

        except json.JSONDecodeError as e:
            return HttpResponseBadRequest('Invalid JSON data')
    else:
        return HttpResponseBadRequest('Only POST requests are allowed')
