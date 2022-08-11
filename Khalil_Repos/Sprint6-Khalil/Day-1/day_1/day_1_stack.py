from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as lam,               # used for: Lambda Function 
    RemovalPolicy,                   # The stack is deleted, so CloudFormation stops managing all resources in it.
  
    Duration,                        # used for: to increase timeout of lambda function at console
    aws_iam as iam_,                 # from grant the access, IAM
    aws_cloudwatch as cloudwatch,    # to use cloudwatch modules , for publish, alarm
    aws_sns as sns,                  # used for: SNS(Simple Notification Service) 
    aws_sns_subscriptions as subscriptions,     # used for : email or lambda or SMS subscriptions
    aws_cloudwatch_actions as actions,          # use to add alarm over  actions 
    aws_apigateway as apiGate                   # Fro REST API
)

from constructs import Construct
from resource import global_instance as gb                      # User define files for global constant

class Day1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        lambda_role=self.createGroupRole()                             # lambda role for full permission for CloudWatch
       
        Notification = sns.Topic(self, "NotifyKhalil")                   # Topic for notification
        Notification.apply_removal_policy(RemovalPolicy.DESTROY)
        
        
                                                # adding email and lambda subscription
        Notification.add_subscription(subscriptions.EmailSubscription("nohrikhalilullah@gmail.com"))            # MAIL
    
    
                    # Api Lambda  from local drive folder
        ApiLambda=self.create_lambda('Khalil-Api-Lambda','./resource','ApiLambda.lambda_handler',lambda_role)    ##invoke API lambda fucntion
        ApiLambda.apply_removal_policy(RemovalPolicy.DESTROY) 
                # Create RestApi InfraStructure:
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/README.html
        api = apiGate.LambdaRestApi(self, "Khalil-restApi-crud",
        handler=ApiLambda, proxy=False)
        urlCRUD = api.root.add_resource("Fetch-Operation")

    # To use lambdaIntegretion: https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/LambdaIntegration.html
        # urlCRUD.add_method("POST",apiGate.MockIntegration(integration_responses=[apiGate.IntegrationResponse(status_code="200")]),method_responses=[apiGate.MethodResponse(status_code="200")])
        urlCRUD.add_method("POST")
                                             # create  each metric
            # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Metric.html
        dimension = {'Arguments' : 'Arguments_'}
        metricAvail = cloudwatch.Metric(metric_name="Argument-Metric", namespace= gb.metricNamespace, dimensions_map= dimension,
        period=Duration.minutes(1),color="#00ff00") # period=Duration(1),The period over which the specified statistic is applied.
       
                                                       # Creating alarm for each metric
            
        alarmAvail =metricAvail.create_alarm(self, id ='Arg-Alarm', evaluation_periods= 1 , threshold= 10,datapoints_to_alarm=1)  # max: Availabilty can be 1
        alarmAvail.add_alarm_action(actions.SnsAction(Notification))
        
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
                # iam_.ServicePrincipal('codebuild.amazonaws.com'),
                iam_.ServicePrincipal("lambda.amazonaws.com"),
                # iam_.ServicePrincipal("sns.amazonaws.com"),
                # iam_.ServicePrincipal("apigateway.amazonaws.com")
                ),
            managed_policies=[
            # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_iam/ManagedPolicy.html
                iam_.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                iam_.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
                iam_.ManagedPolicy.from_aws_managed_policy_name("AWSCloudFormationFullAccess")
            ]
        )
        return role





