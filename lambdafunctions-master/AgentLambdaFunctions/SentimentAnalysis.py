import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    client = boto3.client('dynamodb')
    comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('transcriptTable')
    tableChat = dynamodb.Table('Chat')
    agentUserName = event["Details"]["Parameters"]["AgentUserName"]
    contactId = event["Details"]["ContactData"]["CustomerEndpoint"]["Address"]
    #res=table.scan()
   
    response = table.query(
    KeyConditionExpression=Key('ContactId').eq(contactId)
    )
    print('printing response')
    print(response)
    values=(response['Items'])
    print(values)
    lis=[]
    for item in values:
      lis.append(item['Transcript'])
    data = ' '.join(lis)
    print(data)
    if len(data) == 0:
      data = "Recorded Mhm."
    print(data)
    print('Calling DetectSentiment')
    #result=(json.dumps(comprehend.detect_sentiment(Text=data, LanguageCode='en'), sort_keys=True, indent=4))
    #print (result)
    response= comprehend.detect_sentiment(Text=data, LanguageCode='en')
    print ("Customer Sentiment: "+ response['Sentiment'])
    
    print(agentUserName)
    res=tableChat.scan()
    values=(res['Items'])
    print(values)
    for item in values:
        #agentID=item['AgentID']
        if item['AgentID'] == agentUserName:
          print('Connection Id:  '+item['connectionid'])
          connection_ID = item['connectionid']  
        
    message = {"Sentiment": response['Sentiment']}
    data = {"messages": [message]}
    gatewayapi = boto3.client("apigatewaymanagementapi",
            endpoint_url = 'https://h01v0p99ii.execute-api.us-east-1.amazonaws.com/test')
    gatewayapi.post_to_connection(ConnectionId = connection_ID, Data=json.dumps(data).encode('utf-8')) 
                  
        