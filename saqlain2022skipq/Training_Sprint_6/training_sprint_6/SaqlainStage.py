from constructs import Construct
from aws_cdk import (
    Stage,
    RemovalPolicy,
)

from training_sprint_6.training_sprint_6_stack import TrainingSprint6Stack

class SaqlainStage(Stage):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.stage = TrainingSprint6Stack(self,"SaqlainStage")