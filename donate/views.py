from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import sys
import hashlib
sys.path.insert(1, '../utilities.py')
from utilities import pullFunds, pushFunds, reverseFunds, resolveAlias

@csrf_exempt
def index(request):
    # Filter requests
    if request.method == "GET":
        return HttpResponse("GET REQUEST")
    elif request.method != "POST":
        return JsonResponse({"STATUS": "POST REQUEST ONLY"})

    # TEST DATA
    # amount = "100"
    # senderCardExpiryDate = "2020-10"
    # senderPrimaryAccountNumber = "4957030005123304"
    # recipientPrimaryAccountNumber = "5123280115058611"
    # recipientCardExpiryDate = "2020-11"

    # LOG PRINTS
    print('PRINTING REQUEST BODY')
    print(request.body)

    # PARSE BODIES
    requestBody = json.loads(request.body)
    amount = str(requestBody["amount"])
    senderEmail = str(requestBody["senderEmail"])
    hashedSenderEmail = str(int(hashlib.sha256(senderEmail.encode('utf-8')).hexdigest(), 16))
    recipientEmail = str(requestBody["recipientEmail"])
    hashedRecipientEmail = str(int(hashlib.sha256(recipientEmail.encode('utf-8')).hexdigest(), 16))

    # RESOLVE ALIASES — NORMALLY WOULD USE HASHED EMAIL
    senderPrimaryAccountNumber = resolveAlias('74958889999')
    recipientPrimaryAccountNumber = resolveAlias('74958889999')
    if senderPrimaryAccountNumber == 'ERROR' or recipientPrimaryAccountNumber == 'ERROR':
        return JsonResponse({"STATUS": "BAD REQUEST"})

    # SET PROPER VALUES FOR API CALLS
    senderCardExpiryDate = "2020-11"
    recipientCardExpiryDate = "2020-11"
    senderPrimaryAccountNumber = "4957030005123304"
    recipientPrimaryAccountNumber = "5123280115058611"

    # senderPrimaryAccountNumber = str(requestBody["senderPrimaryAccountNumber"])
    # senderCardExpiryDate = str(requestBody["senderCardExpiryDate"])
    # recipientPrimaryAccountNumber = str(requestBody["recipientPrimaryAccountNumber"])
    # recipientCardExpiryDate = str(requestBody["recipientCardExpiryDate"])

    # PULL FUNDS
    transactionId = pullFunds(
        amount,
        senderPrimaryAccountNumber,
        senderCardExpiryDate
    )
    if transactionId == 'ERROR':
        return JsonResponse({"STATUS": "BAD REQUEST"})

    # PUSH FUNDS
    response = pushFunds(
        str(transactionId),
        amount,
        senderPrimaryAccountNumber,
        senderCardExpiryDate,
        recipientPrimaryAccountNumber,
        recipientCardExpiryDate
    )

    # CHECK PUSH FUNDS ERROR, AND REVERSE IF NEED BE
    if response == 'ERROR':
        reverseFunds(
            str(transactionId),
            amount,
            senderPrimaryAccountNumber,
            senderCardExpiryDate,
        )
        return JsonResponse({"STATUS": "BAD REQUEST"})
    return JsonResponse({"STATUS": "SUCCESS"})
