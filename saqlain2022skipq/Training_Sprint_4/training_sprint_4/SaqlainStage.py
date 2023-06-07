from constructs import Construct
from aws_cdk import (
    Stage,
)

from training_sprint_4.training_sprint_4_stack import TrainingSprint4Stack

class SaqlainStage(Stage):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.stage = TrainingSprint4Stack(self,"SaqlainStage")