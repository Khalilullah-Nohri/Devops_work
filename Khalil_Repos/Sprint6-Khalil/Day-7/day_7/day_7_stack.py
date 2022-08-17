from aws_cdk import (
    aws_s3 as s3,                    # for creating s3 bucket   
    aws_s3_deployment as s3deploy,   # for deployment the s3 bucket
    Stack,                           # the main , for stack
    aws_lambda as lambda_,           # used for: Lambda Function 
    RemovalPolicy,                   # The stack is deleted, so CloudFormation stops managing all resources in it.
    Duration,                        # used for: to increase timeout of lambda function at console
    aws_iam as iam_,                 # from grant the access, IAM
    aws_sns as sns,                  # used for: SNS(Simple Notification Service) 
    aws_sns_subscriptions as subscriptions,     # used for : email or lambda or SMS subscriptions
)


from constructs import Construct

class Day7Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_role=self.createGroupRole()                             # lambda role for full permission for CloudWatch
                                                   
                                                # web health of webs from local drive folder
        WebLambda=self.create_lambda('S3-Files-Khalil','./resource','s3Files.lambda_handler',lambda_role)    ##invoke web health lambda fucntion
        WebLambda.apply_removal_policy(RemovalPolicy.DESTROY)  

    
    
    
    
    def create_lambda(self,id_,asset,handler,lambda_role):                  # lambda function
        return lambda_.Function(self, id_,
        runtime=lambda_.Runtime.PYTHON_3_9,
        handler=handler,
        code=lambda_.Code.from_asset(asset),
        timeout=Duration.seconds(30),
        role=lambda_role
        
        )


# https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_iam/Role.html 
    def createGroupRole(self):
        role=iam_.Role(self,"pipeline-role",
        assumed_by=iam_.CompositePrincipal(
        
                iam_.ServicePrincipal("lambda.amazonaws.com"),
                # iam_.ServicePrincipal("sns.amazonaws.com"),
                ),
            managed_policies=[
            # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_iam/ManagedPolicy.html
                iam_.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                iam_.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
                iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                iam_.ManagedPolicy.from_aws_managed_policy_name("AWSCloudFormationFullAccess")
            ]
        )
        return role