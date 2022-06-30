import aws_cdk as core
import aws_cdk.assertions as assertions
import pytest
from sprint3_khalil.sprint3_khalil_stack import Sprint3KhalilStack

# example tests. To run these tests, uncomment this file along with the example
# resource in sprint3_khalil/sprint3_khalil_stack.py
# def test_sqs_queue_created():
#     app = core.App()
#     stack = Sprint3KhalilStack(app, "sprint3-khalil")
#     template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

@pytest.fixture
# https://docs.pytest.org/en/6.2.x/fixture.html
def template():
    app = core.App()
    stack = Sprint3KhalilStack(app, "sprint3-khalil")
    template = assertions.Template.from_stack(stack)
    return template

# To ignore warnings:  https://stackoverflow.com/questions/40710094/how-to-suppress-py-test-internal-deprecation-warnings
# pytest path-to-test-folder -W ignore::DeprecationWarning  OR pytest -W ignore::DeprecationWarning
def test_create_lambda(template):
    template.resource_count_is("AWS::Lambda::Function",2)   #2 or 4

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


