import aws_cdk as core
import aws_cdk.assertions as assertions

from sprint3_khalil.sprint3_khalil_stack import Sprint3KhalilStack

# example tests. To run these tests, uncomment this file along with the example
# resource in sprint3_khalil/sprint3_khalil_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Sprint3KhalilStack(app, "sprint3-khalil")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
