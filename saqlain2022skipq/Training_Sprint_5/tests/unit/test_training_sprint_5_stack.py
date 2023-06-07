import aws_cdk as core
import aws_cdk.assertions as assertions
import pytest

from training_sprint_5.training_sprint_5_stack import TrainingSprint5Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in training_sprint_5/training_sprint_5_stack.py
# def test_sqs_queue_created():
#     app = core.App()
#     stack = TrainingSprint5Stack(app, "training-sprint-5")
#     template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

''' Unit Test 1 '''
def test_lamda_count():
    app = core.App()
    stack = TrainingSprint5Stack(app, "training-sprint-5")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::Lambda::Function", 3)

''' Unit Test 2 '''
def test_resorces_prop():
    app = core.App()
    stack = TrainingSprint5Stack(app, "training-sprint-5")
    template = assertions.Template.from_stack(stack)
    template.all_resources_properties("AWS::DynamoDB::Table",{"ProvisionedThroughput":assertions.Match.object_like({
                                            "ReadCapacityUnits": 5
                                        })
                                    })

''' Unit Test 3 '''
def test_find_resource():
    app = core.App()
    stack = TrainingSprint5Stack(app, "training-sprint-5")
    template = assertions.Template.from_stack(stack)
    template.find_resources("AWS::Lambda::Function",
                            {
                                "Code": {
                                "S3Bucket": {
                                "Fn::Sub": "cdk-hnb659fds-assets-${AWS::AccountId}-${AWS::Region}"
                                },
                                "S3Key": "e86b614ea80c1526107ee7c337bf3f1ffb49e25c588f7d8d31b6641acccb398f.zip"
                                },
                                "Role": {
                                "Fn::GetAtt": [
                                "LambdaroleD8C079E0",
                                "Arn"
                                ]
                                },
                                "Handler": "WHApp.lambda_handler",
                                "Runtime": "python3.9",
                                "Timeout": 300
                            },   
                            )

''' Unit Test 4 '''
def test_temaplate_matches():
    app = core.App()
    stack = TrainingSprint5Stack(app, "training-sprint-5")
    template = assertions.Template.from_stack(stack)
    template.template_matches({
                                "Resources": 
                                    {"SaqlainTable7141CC55": {
                                    "Type": "AWS::DynamoDB::Table",
                                    "Properties": {
                                        "KeySchema": [
                                        {
                                        "AttributeName": "id",
                                        "KeyType": "HASH"
                                        },
                                        {
                                        "AttributeName": "timestamp",
                                        "KeyType": "RANGE"
                                        }
                                        ],
                                        "AttributeDefinitions": [
                                        {
                                        "AttributeName": "id",
                                        "AttributeType": "S"
                                        },
                                        {
                                        "AttributeName": "timestamp",
                                        "AttributeType": "S"
                                        }
                                        ],
                                        "ProvisionedThroughput": {
                                        "ReadCapacityUnits": 5,
                                        "WriteCapacityUnits": 5
                                        }
                                    },
                                },
                             }
                        })

''' Unit Test 5 '''
def test_lambda_role():
    app = core.App()
    stack = TrainingSprint5Stack(app, "training-sprint-5")
    template = assertions.Template.from_stack(stack)
    template.has_resource_properties("AWS::IAM::Role",
                                        {"AssumeRolePolicyDocument":assertions.Match.object_like({
                                                "Statement": [
                                                {
                                                "Action": "sts:AssumeRole",
                                                "Effect": "Allow",
                                                "Principal": {
                                                    "Service": "lambda.amazonaws.com"
                                                }
                                                }
                                                ],
                                                "Version": "2012-10-17"
                                            }),
                                        })


