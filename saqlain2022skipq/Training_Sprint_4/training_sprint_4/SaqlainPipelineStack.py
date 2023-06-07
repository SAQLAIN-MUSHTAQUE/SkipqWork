import aws_cdk as cdk
from aws_cdk import (
    Stack,
    pipelines as pipelines,
    aws_codepipeline_actions as actions_,
    aws_iam as iam,
)
from constructs import Construct
from training_sprint_4.SaqlainStage import SaqlainStage


class SaqlainPipelineStack(Stack):

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
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/CodeBuildStepProps.html
        synth = pipelines.CodeBuildStep("Synth", 
                                    input = source,
                                    commands = ["ls",
                                                "cd saqlain2022skipq/Training_Sprint_4",
                                                "npm install -g aws-cdk",                        # installing aws-cdk
                                                "pip install -r requirements.txt",               # installing all the libraries for python
                                                "cdk synth",
                                                ],
                                                primary_output_directory = "saqlain2022skipq/Training_Sprint_4/cdk.out"
                                                )
        
        ''' Creating a Pipeline '''
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/CodePipeline.html
        pipeline= pipelines.CodePipeline(self, "saqlainPipelineStack4",synth = synth)  

        ''' Creating Stage '''
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.core/Stage.html
        Alpha = SaqlainStage(self, "Alpha")
        prod = SaqlainStage(self, "Prod")

        pipeline.add_stage(Alpha,
            pre=[
                pipelines.CodeBuildStep("ValidationPoint",
                                        input = source,
                                        commands = ["ls",
                                                    "cd saqlain2022skipq/Training_Sprint_4",
                                                    "npm install -g aws-cdk",             # installing aws-cdk
                                                    "pip install -r requirements.txt",    # installing all the libraries for python
                                                    "pip install -r requirements-dev.txt",
                                                    "pip install boto3",
                                                    "pytest",
                                                    "cd tests",
                                                    "python3 test_integration.py"
                                                    ],
                                                    # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_iam/PolicyStatement.html#aws_cdk.aws_iam.PolicyStatement
                                                    role_policy_statements=[
                                                        iam.PolicyStatement(
                                                            actions=["dynamodb:Scan"],
                                                             resources=["*"]
                                                        )
                                                    ]
                                                )
            ]
        )
        
        pipeline.add_stage(prod,post=[pipelines.ManualApprovalStep("Ready_For_Production")])



