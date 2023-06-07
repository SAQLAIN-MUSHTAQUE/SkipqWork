from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as lambda_,
    aws_iam as iam_,
    RemovalPolicy,
    aws_s3 as s3,
    aws_apigateway as apigateway,
)
from constructs import Construct

class DesignProblem7Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_iam/IRole.html#aws_cdk.aws_iam.IRole
        lambda_role = self.create_lambda_role()

        #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
        fn = self.create_lambda("Saqlain_Payload_app","./Resources","PayloadApp.lambda_handler",lambda_role)
        # Removal Policies:
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
        fn.apply_removal_policy(RemovalPolicy.DESTROY)


        # Creating API gateway
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_apigateway/RestApi.html
        api = apigateway.RestApi(self,'SaqlainS3API')

        # Giving API Handler
        handler = apigateway.LambdaIntegration(fn)

        # Create an API Gateway resource and method for file uploading
        resource = api.root.add_resource('upload')
        resource.add_method('GET', handler)

        # Create an S3 bucket to receive the files
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3/Bucket.html
        bucket = s3.Bucket(self, "SaqlainPayloadBucket",
                            removal_policy=RemovalPolicy.DESTROY,
                            block_public_access=s3.BlockPublicAccess(block_public_policy=False)
                        )
        # # Environment Variable
        fn.add_environment("SaqlainPayloadBucket",bucket.bucket_name)

        # Grant the Lambda function permission to write to the S3 bucket
        bucket.grant_write(fn)


    # Create Lambda 
    def create_lambda(self,id,asset,handler,role):
        return lambda_.Function(self,
            id = id,
            code=lambda_.Code.from_asset(asset),
            handler=handler,
            # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Runtime.html#aws_cdk.aws_lambda.Runtime
            runtime=lambda_.Runtime.PYTHON_3_9,
            timeout = Duration.minutes(10),
            role = role,)    

    # create Lambda Role
    # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_iam/Role.html    
    def create_lambda_role(self):
        
        lambdaRole = iam_.Role(self, "Lambda_role",
            assumed_by=iam_.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam_.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonAPIGatewayInvokeFullAccess"),
                iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
            ])
        return lambdaRole