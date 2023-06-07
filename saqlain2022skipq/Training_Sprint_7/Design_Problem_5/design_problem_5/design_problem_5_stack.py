from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as lambda_,
    aws_iam as iam_,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    RemovalPolicy,
    aws_s3 as s3,
    

)
from aws_cdk.aws_lambda_event_sources import S3EventSource
from constructs import Construct

class DesignProblem5Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_iam/IRole.html#aws_cdk.aws_iam.IRole
        lambda_role = self.create_lambda_role()

        #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
        fn = self.create_lambda("Saqlain_s3_app","./Resources","S3App.lambda_handler",lambda_role)
        # Removal Policies:
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
        fn.apply_removal_policy(RemovalPolicy.DESTROY)
        
        # sns topic
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns/Topic.html
        topic = sns.Topic(self, "SaqlainTopic")
        # topic.add_subscription(subscriptions.LambdaSubscription(fn))
        topic.add_subscription(subscriptions.EmailSubscription("saqlain.mushtaque.skipq@gmail.com"))

        # getting topic.arn
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns/Topic.html#aws_cdk.aws_sns.Topic.topic_arn
        arn = topic.topic_arn 
        fn.add_environment("TopicArn",arn)

        # Create an S3 bucket to receive the files
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3/Bucket.html
        bucket = s3.Bucket(self, "SaqlainBucket",
                            removal_policy=RemovalPolicy.DESTROY,
                            block_public_access=s3.BlockPublicAccess(block_public_policy=False)
                        )
        fn.add_environment("SaqlainBucket",bucket.bucket_name)

        # # Grant S3 permission to trigger the Lambda function
        # bucket.grant_read(fn)


        # Set up an S3 bucket notification to invoke the Lambda function
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda_event_sources/README.html#s3
        fn.add_event_source(S3EventSource(bucket,
            events=[s3.EventType.OBJECT_CREATED],
            filters=[s3.NotificationKeyFilter(prefix="data/")]
        ))
        
    

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
                iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonSNSFullAccess"),
                iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
            ])
        return lambdaRole
