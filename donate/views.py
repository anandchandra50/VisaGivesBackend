from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
# from callapi import callApi
import sys
sys.path.insert(1, '../utilities.py')
from utilities import pullFunds, pushFunds, reverseFunds

@csrf_exempt
def index(request):
    # Pull Funds
    # From the response: take transaction ID
    # We need to translate the sender's email to a card
    # We need these variables:
    # amount, sender card exp date, sender account number (card), recipient card number, recipient card exp date
    if request.method == "GET":
        return HttpResponse("GET REQUEST")
    elif request.method != "POST":
        return JsonResponse({"STATUS": "POST REQUEST ONLY"})
    amount = "100"

    # SENDERS
    # 4895142232120006
    # RECEIVERS
    # 4957030420210496
    # PULL
    # senderPrimaryAccountNumber = "4957030420210454"
    # recipientPrimaryAccountNumber = "4957030420210462"
    # json.loads(request.body)

    # TEST DATA
    senderCardExpiryDate = "2020-10"
    senderPrimaryAccountNumber = "4957030005123304"
    recipientPrimaryAccountNumber = "5123280115058611"
    recipientCardExpiryDate = "2020-11"

    # EXTRACT DATA
    requestBody = json.loads(request.body)
    amount = requestBody["amount"]
    senderPrimaryAccountNumber = requestBody["senderPrimaryAccountNumber"]
    senderCardExpiryDate = requestBody["senderCardExpiryDate"]
    recipientPrimaryAccountNumber = requestBody["recipientPrimaryAccountNumber"]
    recipientCardExpiryDate = requestBody["recipientCardExpiryDate"]


    print('SENDER: {}'.format(senderPrimaryAccountNumber))
    print('RECEIVER: {}'.format(recipientPrimaryAccountNumber))
    transactionId = pullFunds(
        amount,
        senderPrimaryAccountNumber,
        senderCardExpiryDate
    )
    if transactionId == 'ERROR':
        return JsonResponse({"STATUS": "BAD REQUEST"})
    response = pushFunds(
        str(transactionId),
        amount,
        senderPrimaryAccountNumber,
        senderCardExpiryDate,
        recipientPrimaryAccountNumber,
        recipientCardExpiryDate
    )
    if response == 'ERROR':
        reverseFunds(
            str(transactionId),
            amount,
            senderPrimaryAccountNumber,
            senderCardExpiryDate,
        )
        return JsonResponse({"STATUS": "BAD REQUEST"})
    return JsonResponse({"STATUS": "SUCCESS"})
