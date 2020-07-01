import requests
import json
import sys, os
import datetime

date=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
cert=os.path.abspath("./certs/cert.pem")
key=os.path.abspath("./certs/key_test.pem")
headers={"Accept": "application/json"}

user_id='H5T2QIDG2IJOP7L6M1W221bkXTIK_ghOLL4FpzeNLid4v8Mcc'
password='qcgUdXX24YCZENvm54u0kzCk'
timeout=10

def pullFunds(amount, senderPrimaryAccountNumber, senderCardExpiryDate):
    pullFundsUrl='https://sandbox.api.visa.com/visadirect/fundstransfer/v1/pullfundstransactions'
    pullFundsPayload=json.loads('''
    {
    "acquirerCountryCode": "840",
    "acquiringBin": "408999",
    "amount": "'''+amount+'''",
    "businessApplicationId": "AA",
    "cardAcceptor": {
    "address": {
    "country": "USA",
    "county": "081",
    "state": "CA",
    "zipCode": "94404"
    },
    "idCode": "ABCD1234ABCD123",
    "name": "Visa Inc. USA-Foster City",
    "terminalId": "ABCD1234"
    },
    "cavv": "0700100038238906000013405823891061668252",
    "foreignExchangeFeeTransaction": "11.99",
    "localTransactionDateTime": "'''+date+'''",
    "retrievalReferenceNumber": "330000550000",
    "senderCardExpiryDate": "'''+senderCardExpiryDate+'''",
    "senderCurrencyCode": "USD",
    "senderPrimaryAccountNumber": "'''+senderPrimaryAccountNumber+'''",
    "surcharge": "11.99",
    "systemsTraceAuditNumber": "451001",
    "nationalReimbursementFee": "11.22",
    "cpsAuthorizationCharacteristicsIndicator": "Y",
    "addressVerificationData": {
    "street": "XYZ St",
    "postalCode": "12345"
    },
    "settlementServiceIndicator": "9",
    "colombiaNationalServiceData": {
    "countryCodeNationalService": "170",
    "nationalReimbursementFee": "20.00",
    "nationalNetMiscAmountType": "A",
    "nationalNetReimbursementFeeBaseAmount": "20.00",
    "nationalNetMiscAmount": "10.00",
    "addValueTaxReturn": "10.00",
    "taxAmountConsumption": "10.00",
    "addValueTaxAmount": "10.00",
    "costTransactionIndicator": "0",
    "emvTransactionIndicator": "1",
    "nationalChargebackReason": "11"
    },
    "riskAssessmentData": {
    "delegatedAuthenticationIndicator": true,
    "lowValueExemptionIndicator": true,
    "traExemptionIndicator": true,
    "trustedMerchantExemptionIndicator": true,
    "scpExemptionIndicator": true
    },
    "visaMerchantIdentifier": "73625198"
    }
    ''')

    response = requests.post(pullFundsUrl,
                    #   verify = ('put the CA certificate pem file path here'),
    				  cert = (cert,key),
    				  headers = headers,
    				  auth = (user_id, password),
    				#   data = body
                      json=pullFundsPayload,
                      timeout=timeout
                    )
    responseBody = json.loads(response.text)
    print('PULL FUNDS RESPONSE')
    print('------------------')
    print(responseBody)
    print('------------------')
    if responseBody['actionCode'] != '00':
        return 'ERROR'
    else:
        return responseBody['transactionIdentifier']

def pushFunds(transactionId, amount, senderPrimaryAccountNumber, senderCardExpiryDate, recipientPrimaryAccountNumber, recipientCardExpiryDate):
    pushFundsUrl='https://sandbox.api.visa.com/visadirect/fundstransfer/v1/pushfundstransactions'

    pushFundsPayload=json.loads('''
    {
    "acquirerCountryCode": "840",
    "acquiringBin": "408999",
    "amount": "'''+amount+'''",
    "businessApplicationId": "AA",
    "cardAcceptor": {
    "address": {
    "country": "USA",
    "county": "San Mateo",
    "state": "CA",
    "zipCode": "94404"
    },
    "idCode": "CA-IDCode-77765",
    "name": "Visa Inc. USA-Foster City",
    "terminalId": "TID-9999"
    },
    "localTransactionDateTime": "'''+date+'''",
    "merchantCategoryCode": "6012",
    "pointOfServiceData": {
    "motoECIIndicator": "0",
    "panEntryMode": "90",
    "posConditionCode": "00"
    },
    "recipientName": "rohan",
    "recipientPrimaryAccountNumber": "'''+recipientPrimaryAccountNumber+'''",
    "recipientCardExpiryDate": "'''+recipientCardExpiryDate+'''",
    "retrievalReferenceNumber": "412770451018",
    "senderAccountNumber": "'''+senderPrimaryAccountNumber+'''",
    "senderAddress": "901 Metro Center Blvd",
    "senderCity": "Foster City",
    "senderCountryCode": "124",
    "senderName": "Mohammed Qasim",
    "senderReference": "",
    "senderStateCode": "CA",
    "sourceOfFundsCode": "05",
    "systemsTraceAuditNumber": "451018",
    "transactionCurrencyCode": "USD",
    "transactionIdentifier": "'''+transactionId+'''",
    "settlementServiceIndicator": "9",
    "colombiaNationalServiceData": {
    "countryCodeNationalService": "170",
    "nationalReimbursementFee": "20.00",
    "nationalNetMiscAmountType": "A",
    "nationalNetReimbursementFeeBaseAmount": "20.00",
    "nationalNetMiscAmount": "10.00",
    "addValueTaxReturn": "10.00",
    "taxAmountConsumption": "10.00",
    "addValueTaxAmount": "10.00",
    "costTransactionIndicator": "0",
    "emvTransactionIndicator": "1",
    "nationalChargebackReason": "11"
    }
    }
    ''')

    response = requests.post(pushFundsUrl,
                    #   verify = ('put the CA certificate pem file path here'),
    				  cert = (cert,key),
    				  headers = headers,
    				  auth = (user_id, password),
    				#   data = body
                      json=pushFundsPayload,
                      timeout=timeout
                    )
    responseBody = json.loads(response.text)
    print('PUSH FUNDS RESPONSE')
    print('------------------')
    print(responseBody)
    print('------------------')
    if responseBody['actionCode'] != '00':
        return 'ERROR'


def reverseFunds(transactionIdentifier, amount, senderPrimaryAccountNumber, senderCardExpiryDate):
    reverseFundsUrl='https://sandbox.api.visa.com/visadirect/fundstransfer/v1/reversefundstransactions'

    reverseFundsPayload=json.loads('''

    {
    "acquirerCountryCode": "608",
    "acquiringBin": "408999",
    "businessApplicationId": "AA",
    "amount": "'''+amount+'''",
    "cardAcceptor": {
    "address": {
    "country": "USA",
    "county": "San Mateo",
    "state": "CA",
    "zipCode": "94404"
    },
    "idCode": "VMT200911026070",
    "name": "Visa Inc. USA-Foster City",
    "terminalId": "365539"
    },
    "localTransactionDateTime": "'''+date+'''",
    "originalDataElements": {
    "acquiringBin": "408999",
    "approvalCode": "20304B",
    "systemsTraceAuditNumber": "897825",
    "transmissionDateTime": "2020-07-01T13:00:35"
    },
    "pointOfServiceCapability": {
    "posTerminalEntryCapability": "2",
    "posTerminalType": "4"
    },
    "pointOfServiceData": {
    "motoECIIndicator": "0",
    "panEntryMode": "90",
    "posConditionCode": "00"
    },
    "retrievalReferenceNumber": "330000550000",
    "senderCardExpiryDate": "'''+senderCardExpiryDate+'''",
    "senderCurrencyCode": "USD",
    "senderPrimaryAccountNumber": "'''+senderPrimaryAccountNumber+'''",
    "systemsTraceAuditNumber": "451050",
    "transactionIdentifier": "'''+transactionIdentifier+'''",
    "settlementServiceIndicator": "9",
    "colombiaNationalServiceData": {
    "countryCodeNationalService": "170",
    "nationalReimbursementFee": "20.00",
    "nationalNetMiscAmountType": "A",
    "nationalNetReimbursementFeeBaseAmount": "20.00",
    "nationalNetMiscAmount": "10.00",
    "addValueTaxReturn": "10.00",
    "taxAmountConsumption": "10.00",
    "addValueTaxAmount": "10.00",
    "costTransactionIndicator": "0",
    "emvTransactionIndicator": "1",
    "nationalChargebackReason": "11"
    }
    }
    ''')

    response = requests.post(reverseFundsUrl,
                    #   verify = ('put the CA certificate pem file path here'),
    				  cert = (cert,key),
    				  headers = headers,
    				  auth = (user_id, password),
    				#   data = body
                      json=reverseFundsPayload,
                      timeout=timeout
                    )

    responseBody = json.loads(response.text)
    print('REVERSE FUNDS RESPONSE')
    print('------------------')
    print(responseBody)
    print('------------------')
