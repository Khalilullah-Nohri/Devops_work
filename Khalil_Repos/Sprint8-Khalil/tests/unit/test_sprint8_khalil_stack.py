import aws_cdk as core
import aws_cdk.assertions as assertions
import pytest
from sprint8_khalil.sprint8_khalil_stack import Sprint8KhalilStack

# example tests. To run these tests, uncomment this file along with the example
# resource in sprint8_khalil/sprint8_khalil_stack.py
@pytest.fixture
# https://docs.pytest.org/en/6.2.x/fixture.html
def template():
    app = core.App()
    stack = Sprint8KhalilStack(app, "sprint8-khalil")
    template = assertions.Template.from_stack(stack)
    return template
    

# To ignore warnings: [ https://stackoverflow.com/questions/40710094/how-to-suppress-py-test-internal-deprecation-warnings,
# https://docs.pytest.org/en/stable/how-to/capture-warnings.html ]
# Run: pytest path-to-test-folder -W ignore::DeprecationWarning  OR pytest -W ignore::DeprecationWarning
def test_create_lambda(template):
    template.resource_count_is("AWS::Lambda::Function",3)   #2 or 4

def test_create_DYnamo(template):
    template.resource_count_is("AWS::DynamoDB::Table",2)


def test_create_alarm(template):
    template.has_resource("AWS::CloudWatch::Alarm",assertions.Match.any_value())

def test_create_alarm_resource_count(template):
    template.resource_count_is("AWS::IAM::Role",4)

def test_sqs_queue_created(template):
    template.has_resource_properties("AWS::CloudWatch::Alarm", {"ComparisonOperator":"LessThanThreshold"}
    )
