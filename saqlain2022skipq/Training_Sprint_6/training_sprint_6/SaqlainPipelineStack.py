import aws_cdk as cdk
from aws_cdk import (
    Stack,
    pipelines as pipelines,
    aws_codepipeline_actions as actions_,
    aws_iam as iam,
    aws_codebuild as codebuild,
    aws_ecr as ecr,
)
from constructs import Construct
from training_sprint_6.SaqlainStage import SaqlainStage


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
                                                "cd saqlain2022skipq/Training_Sprint_6",
                                                "npm install -g aws-cdk",                        # installing aws-cdk
                                                "pip install boto3",
                                                "pip install -r requirements.txt",               # installing all the libraries for python
                                                "pip install -r requirements-dev.txt",
                                                "cdk synth",
                                                ],
                                                primary_output_directory = "saqlain2022skipq/Training_Sprint_6/cdk.out"
                                                )
        
        ''' Creating a Pipeline '''
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/CodePipeline.html
        pipeline= pipelines.CodePipeline(self, "saqlainPipelineStack6",synth = synth)  

        ''' Creating Stage '''
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.core/Stage.html
        Alpha = SaqlainStage(self, "Alpha")

        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/AddStageOpts.html#aws_cdk.pipelines.AddStageOpts.pre
        pipeline.add_stage(Alpha,
            pre=[
                pipelines.CodeBuildStep("Testing",
                                        input = source,
                                        commands = ["ls",
                                                    "cd saqlain2022skipq/Training_Sprint_6",
                                                    "npm install -g aws-cdk",             # installing aws-cdk
                                                    "pip install -r requirements.txt",    # installing all the libraries for python
                                                    "pip install -r requirements-dev.txt",
                                                    "pip install boto3",
                                                    "pytest",
                                                ],
                                                    
                                            )
                                        ],
                    
            # post=[
            #     pipelines.CodeBuildStep("SaqlainPyresttest", commands=[],
            #                         build_environment=codebuild.BuildEnvironment(
            #                             build_image=codebuild.LinuxBuildImage.from_asset(self, "Image", directory="./pyrestest_crud_api").from_docker_registry(name="docker:dind"),
            #                             privileged=True
            #                         ),
            #                         partial_build_spec=codebuild.BuildSpec.from_object(
            #                             {
            #                                 "version": 0.2,
            #                                 "phases": {
            #                                     "install": {
            #                                         "commands": [
            #                                             "nohup /usr/local/bin/dockerd --host=unix:///var/run/docker.sock --host=tcp://127.0.0.1:2375 --storage-driver=overlay2 &",
            #                                             "timeout 200 sh -c \"until docker info; do echo .; sleep 1; done\""
            #                                         ]
            #                                     },
            #                                     "pre_build": {
            #                                         "commands": [
            #                                             "ls",
            #                                             "cd saqlain2022skipq/Training_Sprint_6/pyrestest_crud_api/",
            #                                             "docker build -t crud_test ."
            #                                         ]
            #                                     },
            #                                     "build": {
            #                                         "commands": [
            #                                             "ls",
            #                                             "docker images",
            #                                             "docker run crud_test"
            #                                         ]
            #                                     }
            #                                 }
            #                             }
            #                         )
            #                         )
            #                     ],
        
                            )

        prod = SaqlainStage(self, "Prod")
        pipeline.add_stage(prod,
            pre=[pipelines.ManualApprovalStep("Ready_For_Production")])


