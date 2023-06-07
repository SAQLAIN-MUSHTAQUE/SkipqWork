import aws_cdk as core
from training_sprint_6.training_sprint_6_stack import TrainingSprint6Stack

def test_sqs_queue_created():
    app = core.App()
    stack = TrainingSprint6Stack(app, "training-sprint-6")
    functions = stack.creat_DynamoDbCRUDTable
    assert functions is not None