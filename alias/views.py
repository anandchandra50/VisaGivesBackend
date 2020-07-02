from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import sys
import hashlib
sys.path.insert(1, '../utilities.py')
from utilities import createAlias, resolveAlias

@csrf_exempt
def index(request):
    if request.method == "GET":
        return HttpResponse("GET REQUEST")
    elif request.method != "POST":
        return JsonResponse({"STATUS": "POST REQUEST ONLY"})
    requestBody = json.loads(request.body)

    email = requestBody['email']
    recipientPrimaryAccountNumber = str(requestBody['recipientPrimaryAccountNumber'])
    hashedEmail = str(int(hashlib.sha256(email.encode('utf-8')).hexdigest(), 16))

    guid = createAlias(hashedEmail, recipientPrimaryAccountNumber)
    if guid == 'ERROR':
        return JsonResponse({'STATUS': 'BAD REQUEST'})
    return JsonResponse({'STATUS': 'SUCCESS'})
