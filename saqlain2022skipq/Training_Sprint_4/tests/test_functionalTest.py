import aws_cdk as core
from training_sprint_4.training_sprint_4_stack import TrainingSprint4Stack

def test_sqs_queue_created():
    app = core.App()
    stack = TrainingSprint4Stack(app, "training-sprint-4")
    functions = stack.creat_DynamoDBTable
    assert functions is not None