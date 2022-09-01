

import boto3                    # For python SDK                    
import json                     # for JSON file 
import os                       # to invoke environment varaible

def lambda_handler(event, context):
    
# https://aws.amazon.com/blogs/database/how-to-use-amazon-dynamodb-global-tables-to-power-multiregion-architectures/
    dynamodb = boto3.resource('dynamodb')
    
    TableName=os.getenv("tableName")                    # fetching TableName 
    table=dynamodb.Table(TableName)                                 
    
                        # Fetch records from JSON
    ResponseID  = event['Records'][0]['Sns']['MessageId']
    Type        = event['Records'][0]['Sns']['Type']
    messageStr  = event['Records'][0]['Sns']['Message']
    message     = json.loads(messageStr)
    metricName  = message['Trigger']['MetricName']
    alarmName   = message['AlarmName']
    timeStamp   = event['Records'][0]['Sns']['Timestamp']
    url         = message['Trigger']['Dimensions'][0]['value']
    nameSpace   = message['Trigger']['Namespace']
    
                    # put_item()  for insert the record into DYNamo DB 
    # https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.html
    table.put_item(
    Item={
        'partitionKey': ResponseID,
        'sortKey'     : messageStr,
        'MetricName'  : metricName,
        'TimeStamp'   : timeStamp,
        'Type'        : Type,
        'URL'         : url,
        'Name Space'  : nameSpace
        }
        )
    
    return "Successfully, Insert the Record..."
    # return event