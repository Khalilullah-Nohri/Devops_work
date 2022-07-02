import aws_cdk as core
import aws_cdk.assertions as assertions
import pytest
from sprint3_khalil.sprint3_khalil_stack import Sprint3KhalilStack


@pytest.fixture
# https://docs.pytest.org/en/6.2.x/fixture.html
def template():
    app = core.App()
    stack = Sprint3KhalilStack(app, "sprint3-khalil")
    template = assertions.Template.from_stack(stack)
    return template
    

# To ignore warnings: [ https://stackoverflow.com/questions/40710094/how-to-suppress-py-test-internal-deprecation-warnings,
# https://docs.pytest.org/en/stable/how-to/capture-warnings.html ]
# Run: pytest path-to-test-folder -W ignore::DeprecationWarning  OR pytest -W ignore::DeprecationWarning
def test_create_lambda(template):
    template.resource_count_is("AWS::Lambda::Function",2)   #2 or 4

def test_create_DYnamo(template):
    template.resource_count_is("AWS::DynamoDB::Table",1)


def test_create_alarm(template):
    template.has_resource("AWS::CloudWatch::Alarm",assertions.Match.any_value())

def test_create_alarm_resource_count(template):
    template.resource_count_is("AWS::IAM::Role",3)

def test_sqs_queue_created(template):
    template.has_resource_properties("AWS::CloudWatch::Alarm", {"ComparisonOperator":"LessThanThreshold"}
    )
    
# def test_has_resource(template):
#     template.template_matches({
#     "Resource": {
#                 "Fn::Join": [
#                   "",
#                   [
#                     "arn:*:iam::",
#                     {
#                       "Ref": "AWS::AccountId"
#                     },
#                     ":role/*"
#                   ]
#                 ]
#     }
# })
    
