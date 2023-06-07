from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as lambda_,
    aws_iam as iam_,
    RemovalPolicy,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_logs as logs,
    aws_logs_destinations as destinations,

)
from constructs import Construct

class DesignProblem6Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_iam/IRole.html#aws_cdk.aws_iam.IRole
        lambda_role = self.create_lambda_role()

        #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
        fn = self.create_lambda("SaqlainDesign6","./Resources","Application.lambda_handler",lambda_role)
        # Removal Policies:
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
        fn.apply_removal_policy(RemovalPolicy.DESTROY)

        # SNS Topic
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns/Topic.html

        # User Topic
        user_topic = sns.Topic(self,"user")

        # Subscription for user topic
        user_topic.add_subscription(subscriptions.EmailSubscription("saqlain.mushtaque.skipq@gmail.com"))

        # getting topic.arn
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns/Topic.html#aws_cdk.aws_sns.Topic.topic_arn
        user_arn = user_topic.topic_arn
        fn.add_environment("UserArn",user_arn)

        # Admin Topic
        Admin_topic = sns.Topic(self,"Admin")

        # Subscription for Admin topic
        Admin_topic.add_subscription(subscriptions.EmailSubscription("mushtaquesaqlain@gmail.com"))

        # getting topic.arn
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns/Topic.html#aws_cdk.aws_sns.Topic.topic_arn
        Admin_arn = Admin_topic.topic_arn
        fn.add_environment("AdminArn",Admin_arn)

        # Grant permissions to the Lambda function to read logs
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_logs/LogGroup.html#aws_cdk.aws_logs.LogGroup.from_log_group_arn
        log_group = logs.LogGroup.from_log_group_arn(
            self, 'LogGroup', log_group_arn='arn:aws:logs:us-east-2:315997497220:log-group:/aws/lambda/SaqlainDesignProblem7Stac-SaqlainPayloadapp12BF556-Zu4bdSBrSMyp:*'
        )

        # CloudWatch Logs subscription filter
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_logs/SubscriptionFilter.html    
        logs.SubscriptionFilter(self, "LogFilter",
            log_group=log_group,
            destination=destinations.LambdaDestination(fn),
            filter_pattern=logs.FilterPattern.all_terms(),
        )

        log_group.grant_read(fn)



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
                iam_.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess")
            ])
        
        return lambdaRole