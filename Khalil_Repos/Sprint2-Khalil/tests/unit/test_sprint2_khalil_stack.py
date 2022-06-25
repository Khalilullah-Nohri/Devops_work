import aws_cdk as core
import aws_cdk.assertions as assertions

from sprint2_khalil.sprint2_khalil_stack import Sprint2KhalilStack

# example tests. To run these tests, uncomment this file along with the example
# resource in sprint2_khalil/sprint2_khalil_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Sprint2KhalilStack(app, "sprint2-khalil")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
