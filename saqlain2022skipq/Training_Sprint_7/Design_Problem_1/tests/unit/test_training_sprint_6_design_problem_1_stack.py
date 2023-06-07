import aws_cdk as core
import aws_cdk.assertions as assertions

from training_sprint_6_design_problem_1.training_sprint_6_design_problem_1_stack import TrainingSprint6DesignProblem1Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in training_sprint_6_design_problem_1/training_sprint_6_design_problem_1_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = TrainingSprint6DesignProblem1Stack(app, "training-sprint-6-design-problem-1")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
