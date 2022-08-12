from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as lam,               # used for: Lambda Function 
    RemovalPolicy,                   # The stack is deleted, so CloudFormation stops managing all resources in it.
    aws_dynamodb as DB,                         # For Dynamo DB module 
    Duration,                        # used for: to increase timeout of lambda function at console
    aws_iam as iam_,                 # from grant the access, IAM
    aws_apigateway as apiGate                   # Fro REST API
)

from constructs import Construct


class Day2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # The code that defines your stack goes here

        lambda_role=self.createGroupRole()                             # lambda role for full permission for CloudWatch
       
    
                    # Api Lambda  from local drive folder
        ApiLambda=self.create_lambda('Khalil-Api-Lambda','./resource','ApiLambda.lambda_handler',lambda_role)    ##invoke API lambda fucntion
        ApiLambda.apply_removal_policy(RemovalPolicy.DESTROY) 
        
        
        global_crud_table = DB.Table(self, "DynamoDBCRUDTable", partition_key=DB.Attribute(name="AttributeValue", type=DB.AttributeType.STRING),
        sort_key=DB.Attribute(name="TimeStamp_", type=DB.AttributeType.STRING))
        global_crud_table.apply_removal_policy(RemovalPolicy.DESTROY)                
        
        
        table_name=global_crud_table.table_name                                              
        ApiLambda.add_environment("CRUDtableName" ,table_name)             # add Table name as an  environmental variable
        

        
        
        
                # Create RestApi InfraStructure:
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/README.html
        
        api = apiGate.LambdaRestApi(self, "Khalil-restApi-crud",
        handler=ApiLambda, proxy=False)
        
        urlCRUD = api.root.add_resource("Fetch-Operation")

        # urlCRUD.add_method("POST",apiGate.MockIntegration(integration_responses=[apiGate.IntegrationResponse(status_code="200")]),method_responses=[apiGate.MethodResponse(status_code="200")])
        urlCRUD.add_method("POST")
        urlCRUD.add_method("GET")
        
        api2 = apiGate.LambdaRestApi(self, "Khalil-2ndrestApi-crud",
        handler=ApiLambda, proxy=False)
        
        urlCRUD = api2.root.add_resource("Fetch-Operation")

        # urlCRUD.add_method("POST",apiGate.MockIntegration(integration_responses=[apiGate.IntegrationResponse(status_code="200")]),method_responses=[apiGate.MethodResponse(status_code="200")])
        urlCRUD.add_method("POST")
        urlCRUD.add_method("GET")
        
        
                # Lambda Construct
# https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Function.html?highlight=add_environment#aws_cdk.aws_lambda.Function
    def create_lambda(self,id_,asset,handler,lambda_role):
        return lam.Function(self, id_,
        runtime=lam.Runtime.PYTHON_3_9,
        handler=handler,
        code=lam.Code.from_asset(asset),
        timeout=Duration.seconds(30),
        role=lambda_role)
        
# https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_iam/Role.html 
    def createGroupRole(self):
        role=iam_.Role(self,"pipeline-role",
        assumed_by=iam_.CompositePrincipal(
            # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_iam/ServicePrincipal.html
                iam_.ServicePrincipal("lambda.amazonaws.com"),
                ),
            managed_policies=[
                iam_.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess")
            ]
        )
        return role





