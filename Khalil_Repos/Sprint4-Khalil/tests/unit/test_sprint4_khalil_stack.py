import aws_cdk as core
import aws_cdk.assertions as assertions

from sprint4_khalil.sprint4_khalil_stack import Sprint4KhalilStack

# example tests. To run these tests, uncomment this file along with the example
# resource in sprint4_khalil/sprint4_khalil_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Sprint4KhalilStack(app, "sprint4-khalil")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
