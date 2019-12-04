import json
import boto3
from boto3.dynamodb.conditions import Key, Attr


def lambda_handler(event, context):
    client = boto3.client('dynamodb')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('CustomerHistory')
    contactId = event["Details"]["ContactData"]["CustomerEndpoint"]["Address"]
    print(contactId)
    response = table.query(
    KeyConditionExpression=Key('CustomerPhoneNo').eq(int(contactId))
    )
    print('printing response')
    print(response)
    value=(response['Items'])
    if len(value) == 0:
        value = [{'CustomerPhoneNo': '1918071017000', 'CustomerName': 'Harry'}]
    #print(value[0]['CustomerName'])
    print(value)
    return value[0]