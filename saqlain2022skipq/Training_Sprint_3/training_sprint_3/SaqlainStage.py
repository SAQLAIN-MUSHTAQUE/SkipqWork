from constructs import Construct
from aws_cdk import (
    Stage,
)

from training_sprint_3.training_sprint_3_stack import TrainingSprint3Stack

class SaqlainStage(Stage):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.stage = TrainingSprint3Stack(self,"SaqlainStage")