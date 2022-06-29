import aws_cdk as core
import aws_cdk.assertions as assertions
# from aws_cdk.assertions import Template
from sprint3_khalil.sprint3_khalil_stack import Sprint3KhalilStack

# example tests. To run these tests, uncomment this file along with the example
# resource in sprint3_khalil/sprint3_khalil_stack.py
# def test_sqs_queue_created():
#     app = core.App()
#     stack = Sprint3KhalilStack(app, "sprint3-khalil")
#     template = assertions.Template.from_stack(stack)

def test_create_lambda():
    app = core.App()
    stack = Sprint3KhalilStack(app, "sprint3-khalil")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::Lambda::Function",2)   #2 or 4

# import warnings


# def api_v1():
#     warnings.warn(UserWarning("api v1, should use functions from v2"))
#     return 1


# def test_one():
#     assert api_v1() == 1

# def test_create_DYnamo():
#     app = core.App()
#     stack = Sprint3KhalilStack(app, "sprint3-khalil")
#     template = assertions.Template.from_stack(stack)

#     template.resource_count_is("AWS::DynamoDB::Table",1)


# def test_create_alarm():
#     app = core.App()
#     stack = Sprint3KhalilStack(app, "sprint3-khalil")
#     template = assertions.Template.from_stack(stack)
#     template.has_resource("AWS::CloudWatch::Alarm",assertions.Match.any_value())
    # template.resource_count_is("AWS::IAM::Role",1)


# def test_sqs_queue_created():
#     app = core.App()
#     stack = Sprint3KhalilStack(app, "sprint3-khalil")
#     template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
