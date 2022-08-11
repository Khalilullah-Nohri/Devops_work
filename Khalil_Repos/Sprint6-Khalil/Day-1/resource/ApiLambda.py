import boto3                    # For python SDK                    
import json                     # for JSON file 
import logging 

import global_instance as gb

from  cloudwatch import cloud_watch
cw_obj=cloud_watch()

logger = logging.getLogger(); 
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    
    
    crudOperation=event["httpMethod"]      # Return which CRUD operation/Method is called
    # logger.info(event)
    if crudOperation=="POST":
        response = saveProduct(json.loads(event['body'])) 
    else:
        response = buildResponse (404, 'Not Found')
        
    return response

# All the DynamoDB function's reference is : https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

def saveProduct (requestBody):      # Insert the item in Table
    try:
        avail=int(requestBody['Value'])
        dimension=[{'Name':'Arguments','Value':"Final Values"}]           # A dimension is a name/value pair that is part of the identity of a metric
        cw_obj.publish_metric(nameSpace=gb.metricNamespace,metricName='ArgumentMetric',dimension=dimension,value=avail)
        body={
            "Operation": "Input Values",
            "Message": "Success", 
            "Item": requestBody
        }
        return buildResponse (200, body)                 
    except:
        logger.exception('Exception Occured !!! POST Operation Failed')


def buildResponse(statusCode, body=None): 
    response = {
        'statusCode': statusCode, 
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": '*'
            
        }
    }
    if body is not None:
        response['body'] = json.dumps(body)  # json.dumps() takes in a json object and returns a string.

    return response

