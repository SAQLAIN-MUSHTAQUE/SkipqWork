import aws_cdk as core
import aws_cdk.assertions as assertions

from design_problem_6.design_problem_6_stack import DesignProblem6Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in design_problem_6/design_problem_6_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = DesignProblem6Stack(app, "design-problem-6")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
