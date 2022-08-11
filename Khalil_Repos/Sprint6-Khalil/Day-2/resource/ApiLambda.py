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
        response = saveProduct(json.loads(event['body'][0])) 
    # elif crudOperation=="GET":
    #     response = getProducts()
    # elif crudOperation=="PATCH":
    #     requestBody = json.loads(event['body'])
    #     response = modifyProduct(requestBody["ID"],requestBody["updateValue"])
    # elif crudOperation=="DELETE":
    #     requestBody = json.loads(event['body'])
    #     response = deleteProduct(requestBody['ID'])
    else:
        response = buildResponse (404, 'Not Found')
        
    return response

# All the DynamoDB function's reference is : https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

# def getProducts():                  # Return all the items of Table
#     try:
#         URLsList,URLsID=fetchURLs(table)                               # fetch all URLs which will be insert by client
#         if len(URLsList) != 0:
#             body = {
#                 "products": URLsList
#             }
#             return buildResponse (200, body)
#         else:
#             body = {
#                 "products": "Table is Empty"
#             }
#             return buildResponse (200, body)
#     except:
#         logger.exception('Exception Occured !!! GET Operation Failed')

def saveProduct (requestBody):      # Insert the item in Table
    try:
        # URLsList,URLsID=fetchURLs(table)                               # fetch all URLs which will be insert by client
        # if requestBody["ID"] not in URLsID:                     # First Verify the primaryKey already exist or not
            # if requestBody["URL"] not in URLsList:              # To verify that, URL already exist or not

# datetime object containing current date and time
        now = datetime.now()
        # print("now =", now)

        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        # print("date and time =", dt_string)	

        table.put_item(Item=
        {
            "TimeStamp":dt_string,
            "Value": requestBody['event1']['attr']
        }
        ) 
        body = {
            "Operation": "SAVE",
            "Message": "SUCCESS", 
            "Item": requestBody
        }
        return buildResponse (200, body) 
        #     else:
        #         body={
        #         "Operation": "FAIL",
        #         "Message": "NOT SUCCESS, ALREADY URL IN DATABASE", 
        #         "Item": requestBody
        #     }
        #         return buildResponse (404, body)                 
        # else:
        #     body={
        #         "Operation": "FAIL",
        #         "Message": "NOT SUCCESS, ALREADY ID IN DATABASE", 
        #         "Item": requestBody
        #     }
        #     return buildResponse (404, body) 
    except:
        logger.exception('Exception Occured !!! POST Operation Failed')


    
# def getProduct(productId):                  # Fetch single item on the ID basis 
#     try: 
#         response = table.get_item( Key={
#         "ID": productId
        
#     })
#         if 'Item' in response:
#             # return buildResponse (200, response['Item'])
#             return True
#         else:
#             # return buildResponse (404, {'Message': 'ProductId: %s not found' % productId}) 
#             return False
#     except:
#         logger.exception('Fetch Single Item Failed !!!')
    
    
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

