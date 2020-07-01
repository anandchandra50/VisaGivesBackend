from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
# from callapi import callApi
import sys
sys.path.insert(1, '../utilities.py')
from utilities import pullFunds, pushFunds, reverseFunds

def index(request):
    # Pull Funds
    # From the response: take transaction ID
    # We need to translate the sender's email to a card
    # We need these variables:
    # amount, sender card exp date, sender account number (card), recipient card number, recipient card exp date

    amount = "100"
    senderCardExpiryDate = "2020-10"
    # SENDERS
    # 4895142232120006
    # RECEIVERS
    # 4957030420210496
    # PULL
    # senderPrimaryAccountNumber = "4957030420210454"
    # recipientPrimaryAccountNumber = "4957030420210462"
    senderPrimaryAccountNumber = "4957030005123304"
    recipientPrimaryAccountNumber = "5123280115058611"
    recipientCardExpiryDate = "2020-11"
    print('SENDER: {}'.format(senderPrimaryAccountNumber))
    print('RECEIVER: {}'.format(recipientPrimaryAccountNumber))
    transactionId = pullFunds(
        amount,
        senderPrimaryAccountNumber,
        senderCardExpiryDate
    )
    if transactionId == 'ERROR':
        return HttpResponseNotFound("BAD REQUEST")
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
        return HttpResponseNotFound("BAD REQUEST")
    return HttpResponse("SUCCESS")
