import aws_cdk as core
import aws_cdk.assertions as assertions

from day_2.day_2_stack import Day2Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in day_2/day_2_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Day2Stack(app, "day-2")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
