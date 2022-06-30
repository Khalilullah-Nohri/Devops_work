from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as lam,               # used for: Lambda Function 
    RemovalPolicy,                   # The stack is deleted, so CloudFormation stops managing all resources in it.
    aws_events as events,            # used for: events like  schedule
    aws_events_targets as targets,   # used for: to target the events
    Duration,                        # used for: to increase timeout of lambda function at console
    aws_iam as iam_,                 # from grant the access, IAM
    aws_cloudwatch as cloudwatch,    # to use cloudwatch modules , for publish, alarm
    aws_sns as sns,                  # used for: SNS(Simple Notification Service) 
    aws_sns_subscriptions as subscriptions,     # used for : email or lambda or SMS subscriptions
    aws_cloudwatch_actions as actions,          # use to add alarm over  actions 
    aws_dynamodb as DB,                         # For Dynamo DB module 
    aws_codedeploy as codedeploy
)
from constructs import Construct
from resource import global_instance as gb                      # User define files for global constant


class Sprint3KhalilStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
    
        lambda_role=self.createGroupRole()                             # lambda role for full permission for CloudWatch
    
                    # web health of webs from local drive folder
        WebLambda=self.create_lambda('Web-Health-Khalil','./resource','webHealthLambda.lambda_handler',lambda_role)    ##invoke web health lambda fucntion
        WebLambda.apply_removal_policy(RemovalPolicy.DESTROY) 
        
        
        Notification = sns.Topic(self, "NotifyKhalil")                   # Topic for notification
        Notification.apply_removal_policy(RemovalPolicy.DESTROY)
        
        
                                                # adding email and lambda subscription
        Notification.add_subscription(subscriptions.EmailSubscription("nohrikhalilullah@gmail.com"))            # MAIL
        Notification.add_subscription(subscriptions.SmsSubscription("+923421520614"))                           # SMS
        
        
        
        for web in gb.URL_TO_MONITOR:
            dimension = {'URL' : web}
                                                # create  each metric
            # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Metric.html
            metricAvail = cloudwatch.Metric(metric_name=gb.availMetric   + " : "+web, namespace= gb.metricNamespace, dimensions_map= dimension, period=Duration.minutes(1),color="#00ff00") # period=Duration(1),The period over which the specified statistic is applied.
            metricLat   = cloudwatch.Metric(metric_name=gb.latencyMetric + " : "+web, namespace= gb.metricNamespace, dimensions_map= dimension, period=Duration.minutes(1),color="#0000ff")
            
                                                # Creating alarm for each metric
            
            alarmAvail =metricAvail.create_alarm(self, id ='avail'   + web, evaluation_periods= 1 , threshold= 1,
                                                comparison_operator=cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD )  # max: Availabilty can be 1
            # alarmAvail =metricAvail.create_alarm(self, id ='avail'   + web, evaluation_periods= 1 , threshold= 1.5)   # evvalution_periods:The number of periods over which data is compared to the specified threshold., threshold:The value against which the specified statistic is compared
            alarmLat   =metricLat.create_alarm(self, id = 'latency ' + web, evaluation_periods= 1 , threshold= 0.3)      # min: latency can be 0
            
            # adding an alarm for  action after such cross of threshold value
            alarmAvail.add_alarm_action(actions.SnsAction(Notification))
            alarmLat.add_alarm_action  (actions.SnsAction(Notification))         
        
        
                                            # Create DynamoDB table to store alarm logs of generated alarms
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_dynamodb/Table.html
        
        # For partition_key and sort_key : see, https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_dynamodb/Attribute.html#aws_cdk.aws_dynamodb.Attribute
        global_table = DB.Table(self, "DynamoDBTable", partition_key=DB.Attribute(name="partitionKey", type=DB.AttributeType.STRING),sort_key=DB.Attribute(name="sortKey", type=DB.AttributeType.STRING) )
        global_table.apply_removal_policy(RemovalPolicy.DESTROY)                
        
        # DBlambdaRole=self.createGroupRole()                                # IAM role to DYNamo DB
        DBLambda=self.create_lambda('DB-Lambda','./resource','DBLambda.lambda_handler',lambda_role)
        
        table_name=global_table.table_name                                              
        DBLambda.add_environment("tableName" ,table_name )                              # add Table name as an  environmental variable
        Notification.add_subscription(subscriptions.LambdaSubscription(fn = DBLambda))
       
       
       
                                #   failure metric for the one metric
        # One way to create failure metric 
        # failureMetric = cloudwatch.Metric(namespace= "AWS/Lambda",metric_name="Duration", dimensions_map= {"FunctionName":WebLambda.function_name})
        # failureMetric =WebLambda.metric_duration(period=Duration.minutes(5))
        

        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Function.html  
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Alarm.html
                                        # set alarm on failure Duration metric
        webHealthfailureAlarm2 = cloudwatch.Alarm(
            self,
            id="Lambda Duration Failure Alarm2",
            metric=WebLambda.metric_duration(period=Duration.minutes(6)),          # How long execution of this Lambda takes. average 5 minutes
            #The period over which the specified statistic is applied. Default: Duration.minutes(5)
            evaluation_periods = 1,
            threshold=2500
        )
        
                                        # set alarm on failure Invocations metric
        webHealthfailureAlarm = cloudwatch.Alarm(
            self,
            id="Lambda Invocayions Failure Alarm",
            metric=WebLambda.metric_invocations(period=Duration.minutes(7)),   # How often this Lambda is invoked. Sum over 5 minutes
            comparison_operator = cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
            evaluation_periods = 1,
            threshold=1
        )

        # Create Alarms to monitor health of FO DynamoDB
                            # Create alarm for Duration
        DynamoDBfailureAlarm = cloudwatch.Alarm(
            self,
            id="DynamoDB Duration Failure Alarm",
            metric=DBLambda.metric_duration(period=Duration.minutes(5)),       #  
            comparison_operator = cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            evaluation_periods = 1,
            threshold=2500
        )
        # Create alarms for Invocations
        DynamoDBfailureAlarm2 = cloudwatch.Alarm(
            self,
            id="DynamoDB Invocayions Failure Alarm2",
            metric=DBLambda.metric_invocations(period=Duration.minutes(5)),
            comparison_operator = cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
            evaluation_periods = 1,
            threshold=1
        )
        
        
        
        
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Function.html
                               # Alias for current version of Lambda
        webHealthalias=lam.Alias(self,"Failure_Alarm_WebHealth_Khalil",alias_name="current_version_WebHealth_one",version=WebLambda.current_version)       # A new alias to a particular version of a Lambda function
        aliasDynampDB=lam.Alias(self,"Failure_Alarm_DynamoDB_Khalil",alias_name="current_version_DynamoDB_one",version=DBLambda.current_version)       # A new alias to a particular version of a Lambda function
        
        # Code Deployment Group : AWS CodeDeploy is a deployment service that automates application deployments to Amazon EC2 instances, on-premises instances, serverless Lambda functions, or Amazon ECS services.
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_codedeploy/LambdaDeploymentGroup.html
        deployment_group=codedeploy.LambdaDeploymentGroup(self,"CodeDeployment_WebHealth_Khalil", alias=webHealthalias,
        deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_2_MINUTES,alarms=[webHealthfailureAlarm,webHealthfailureAlarm2]      # LambdaDeploymentConfig: A custom Deployment Configuration for a Lambda Deployment Group.                    
            )                                                                                                         # ALSO, CANARY_10_PERCENT_10_MINUTES  https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_codedeploy/LambdaDeploymentConfig.html?highlight=canary_10_percent_10_minutes#aws_cdk.aws_codedeploy.LambdaDeploymentConfig.CANARY_10_PERCENT_10_MINUTES                            
        deployment_group2=codedeploy.LambdaDeploymentGroup(self,"CodeDeployment_DynamoDB_Khalil", alias=aliasDynampDB,
        deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_2_MINUTES,alarms=[DynamoDBfailureAlarm,DynamoDBfailureAlarm2])


       
        
                #To Cron the web health lambda
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_events/Schedule.html
        #  day=None, hour=None, minute=None, month=None, week_day=None, year=None
        schedule=events.Schedule.cron()       # to trigger the event after 1MINT ..........to change..    .cron(minute="1", hour="0")
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_events/Rule.html
        rule = events.Rule(self, "Schedule Rule", schedule=schedule) 
        
        # add webhealth as a target for rule
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_events_targets/LambdaFunction.html
        rule.add_target(targets.LambdaFunction(handler=WebLambda))
        
        
        

# Lambda Construct
# https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Function.html?highlight=add_environment#aws_cdk.aws_lambda.Function
    def create_lambda(self,id_,asset,handler,lambda_role):
        return lam.Function(self, id_,
        runtime=lam.Runtime.PYTHON_3_6,
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
                # iam_.ServicePrincipal("sns.amazonaws.com")
                ),
            managed_policies=[
            # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_iam/ManagedPolicy.html
                iam_.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                iam_.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
                iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"),
                iam_.ManagedPolicy.from_aws_managed_policy_name("AwsCloudFormationFullAccess")
            ]
        )
        return role