import aws_cdk as core
import aws_cdk.assertions as assertions

from training_sprint_3.training_sprint_3_stack import TrainingSprint3Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in training_sprint_3/training_sprint_3_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = TrainingSprint3Stack(app, "training-sprint-3")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
