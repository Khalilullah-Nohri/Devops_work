import aws_cdk as core
import aws_cdk.assertions as assertions

from day_1.day_1_stack import Day1Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in day_1/day_1_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Day1Stack(app, "day-1")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
