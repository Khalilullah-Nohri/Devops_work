import boto3,os

# dynamodb = boto3.resource('dynamodb')
# TableName=os.getenv("CRUDtableName")                    # fetching TableName 
# tableName=dynamodb.Table(TableName)

def fetchURLs(tableName):
    response = tableName.scan()
    result = response['Items']
        
        # If all Items not be scanned in above method then we use while loop.
        # LastEvaluatedkey: when all items not scanned it returns attribute of LastEvaluatedKey in response ,then 
        # with help of ExclusiveStartKey we will expand items in response, So simply it means If DynamoDB processes the number
        # of items up to the limit while processing the results, it stops the operation and returns the matching values up to that 
        # point, and a key in LastEvaluatedKey to apply in a subsequent operation, so that you can pick up where you left off.
        # ExclusiveStartkey; he primary key of the first item that this operation will evaluate. Use the value 
        # that was returned for LastEvaluatedKey in the previous operation. 
    
    while 'LastEvaluatedkey' in response:
        response = tableName.scan(ExclusiveStartkey=response['LastEvaluatedKey'])
        result.extend(response['Item'])
    
    # result=sorted(result.items())
    # dict(sorted(result.items(), key=lambda item: item[1]))
    
    URLsList,partitionKey=[],[]
    for index in range(len(result)):
        URLsList.append(result[index]["URL"])
        partitionKey.append(result[index]["ID"])
    return URLsList,partitionKey
    