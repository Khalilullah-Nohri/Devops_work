from aws_cdk import (
    # Duration,
    # aws_sqs as sqs,
    Stack,
    aws_lambda as lam,                # used for: Lambda Function
    Duration,                         # used for: to increase timeout of lambda function at console
    RemovalPolicy,                    # The stack is deleted, so CloudFormation stops managing all resources in it.
)
from constructs import Construct

class Sprint1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        HWLambda=self.create_lambda('Khalilullah','./resource','helloLambdaFunction.lambda_handler')      # For SImple Hello world message
        HWLambda.apply_removal_policy(RemovalPolicy.DESTROY)                                              # to destory the stack from console
  




    def create_lambda(self,id_,asset,handler):
        return lam.Function(self, id_,
        runtime=lam.Runtime.PYTHON_3_6,
        handler=handler,
        code=lam.Code.from_asset(asset),
        timeout=Duration.seconds(30))