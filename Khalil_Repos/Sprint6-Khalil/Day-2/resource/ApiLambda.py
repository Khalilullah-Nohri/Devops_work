import boto3                    # For python SDK                    
import json                     # for JSON file 
import os                       # to invoke environment varaible
import logging 

from datetime import datetime
from fetchClientURLs import fetchURLs

logger = logging.getLogger(); 
logger.setLevel(logging.INFO)

# For Os-environement: https://aws.amazon.com/blogs/database/how-to-use-amazon-dynamodb-global-tables-to-power-multiregion-architectures/
dynamodb = boto3.resource('dynamodb')
TableName=os.getenv("CRUDtableName")                    # fetching TableName 
table=dynamodb.Table(TableName)



def lambda_handler(event, context):
    
    
    crudOperation=event["httpMethod"]      # Return which CRUD operation/Method is called
    # logger.info(event)
    if crudOperation=="POST":
        event_=event['body']
        response = saveProduct(json.loads(event_)) 
    elif crudOperation=="GET":
        response = getProducts()

    else:
        response = buildResponse (404, 'Not Found')
        
    return response

# All the DynamoDB function's reference is : https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

def getProducts():                  # Return all the items of Table
    try:
        URLsList=fetchURLs(table)                               # fetch all URLs which will be insert by client
        if len(URLsList) != 0:
            body = {
                "Values": URLsList
            }
            return buildResponse (200, body)
        else:
            body = {
                "Values": "Table is Empty..."
            }
            return buildResponse (200, body)
    except:
        logger.exception('Exception Occured !!! GET Operation Failed')

def saveProduct (requestBody):      # Insert the item in Table
    try:

        # datetime object containing current date and time
        currentDateTime = datetime.now()
        dt_string = currentDateTime.strftime("%d/%m/%Y %H:%M:%S")
            
        table.put_item(Item={
            "AttributeValue": dict(requestBody[0])['event1']['attr1'],
            "TimeStamp_":dt_string
            }
        ) 
        body = {
            "Operation": "SAVE",
            "Message": "SUCCESS", 
            "Item": requestBody,
            "InputDate":dt_string,
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

