import boto3
import json
def lambda_handler(event, context):
 table = boto3.resource('dynamodb').Table('Chat')
 connectionId = event["requestContext"]["connectionId"]
 AgentUsername = event["body"]
 print(json.loads(AgentUsername)["AgentID"])
 table.update_item(
    Key={'connectionid': connectionId},
    UpdateExpression='SET AgentID = :val1',
    ExpressionAttributeValues={
        ':val1': json.loads(AgentUsername)["AgentID"]
    }
 )
 return {
    'statusCode': 200,
    'body': json.dumps({'input': event})
}