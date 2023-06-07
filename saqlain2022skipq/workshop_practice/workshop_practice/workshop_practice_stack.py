from constructs import Construct
from aws_cdk import (
    aws_lambda as lambda_,
    Stack,
)


class WorkshopPracticeStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        my_lambda = lambda_.Function(self,
                id = "HelloHandler",
                code = lambda_.Code.from_asset('Resources'),
                handler = 'hello.handler',
                runtime = lambda_.Runtime.PYTHON_3_9,
            )

        

        