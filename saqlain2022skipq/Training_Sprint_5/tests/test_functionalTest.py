import aws_cdk as core
from training_sprint_5.training_sprint_5_stack import TrainingSprint5Stack

def test_sqs_queue_created():
    app = core.App()
    stack = TrainingSprint5Stack(app, "training-sprint-5")
    functions = stack.creat_DynamoDbCRUDTable
    assert functions is not None