import json
import boto3
from boto3.dynamodb.conditions import Key, Attr


def lambda_handler(event, context):
    client = boto3.client('dynamodb')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('CustomerHistory')
    tableChat = dynamodb.Table('Chat')
    agentUserName = event["Details"]["Parameters"]["AgentUserName"]
    contactId = event["Details"]["ContactData"]["CustomerEndpoint"]["Address"]
    #res=table.scan()
    print(contactId)
    response = table.query(
    KeyConditionExpression=Key('CustomerPhoneNo').eq(int(contactId))
    )
    print('printing response')
    print(response)
    value=(response['Items'])
    print(value)
    
    for item in value:
        value = "CustomerPhoneNo :" + str(item['CustomerPhoneNo']) + "," + "CustomerName :" + item["CustomerName"]

    if len(value) == 0:
        value = "CustomerPhoneNo :" + str(contactId) + "," + "CustomerName :" + "Harry"
    print(value)
    #taking out connectionID
    table2 = dynamodb.Table('Chat')
    res=table2.scan()
    values=(res['Items'])
    


    print(agentUserName)
    for item in values:
        #agentID=item['AgentID']
        if item['AgentID'] == agentUserName:
          print('Connection Id:  '+item['connectionid'])
          connection_ID = item['connectionid']  
        
    message = {"CustomerInformation": str(value)}
    data = {"messages": [message]}
    gatewayapi = boto3.client("apigatewaymanagementapi",
            endpoint_url = 'https://h01v0p99ii.execute-api.us-east-1.amazonaws.com/test')
    gatewayapi.post_to_connection(ConnectionId = connection_ID, Data=json.dumps(data).encode('utf-8')) 
                 