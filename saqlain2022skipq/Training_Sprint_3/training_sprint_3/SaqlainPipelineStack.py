import aws_cdk as cdk
from aws_cdk import (
    Stack,
    pipelines as pipelines,
    aws_codepipeline_actions as actions_
)
from constructs import Construct
from training_sprint_3.SaqlainStage import SaqlainStage


class SaqlainpipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ''' Source authentication from GitHub '''
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/CodePipelineSource.html
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk/SecretValue.html
        # https://docs.aws.amazon.com/cli/latest/reference/secretsmanager/create-secret.html
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_codepipeline_actions/GitHubTrigger.html#aws_cdk.aws_codepipeline_actions.GitHubTrigger
        source = pipelines.CodePipelineSource.git_hub("saqlain2022skipq/EaglePython", "main",
                                                        authentication = cdk.SecretValue.secrets_manager("SaqlainToken"),
                                                        trigger = actions_.GitHubTrigger('POLL'),
                                                        )

        '''Adding CodeBuild to synthesize application '''
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/CodePipelineSource.html
        synth = pipelines.CodeBuildStep("Synth", 
                                    input = source,
                                    commands = ["ls",
                                                "cd saqlain2022skipq/Training_Sprint_3",
                                                "npm install -g aws-cdk",                        # installing aws-cdk
                                                "python3 -m pip install -r requirements.txt",    # installing all the libraries for python
                                                "cdk synth",
                                                ],
                                                primary_output_directory = "saqlain2022skipq/Training_Sprint_3/cdk.out"
                                                )
        
        ''' Creating a Pipeline '''
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/CodePipeline.html
        pipeline= pipelines.CodePipeline(self, "saqlainPipelineStack3",synth =   synth)  

        ''' Creating Stage '''
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.core/Stage.html
        preprod = SaqlainStage(self, "Alpha")
        prod = SaqlainStage(self, "Prod")

        pipeline.add_stage(preprod,
        
            post=[
                pipelines.CodeBuildStep("Validation Point",
                    commands=["curl -Ssf https://www.skipq.org/"]
                )
            ]
        )
        
        pipeline.add_stage(prod,pre=[pipelines.ManualApprovalStep("PromoteToProd")])



