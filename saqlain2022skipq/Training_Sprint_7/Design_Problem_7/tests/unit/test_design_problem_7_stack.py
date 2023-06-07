import aws_cdk as core
import aws_cdk.assertions as assertions

from design_problem_7.design_problem_7_stack import DesignProblem7Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in design_problem_7/design_problem_7_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = DesignProblem7Stack(app, "design-problem-7")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
