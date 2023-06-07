from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as lambda_,
    aws_events as events,
    aws_events_targets as targets,
    RemovalPolicy,
    aws_cloudwatch as cw,
    aws_iam as iam_,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_cloudwatch_actions as cw_actions,
    aws_dynamodb as db,
)

from constructs import Construct
from Resources import constants as constant
import os

class TrainingSprint3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_iam/IRole.html#aws_cdk.aws_iam.IRole
        lambda_role = self.create_lambda_role()

        """Section For Lambda Function"""
        #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
        WHApp_Lambda = self.create_lambda("Saqlain_WHL_App","./Resources","WHApp.lambda_handler",lambda_role)
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
        WHApp_Lambda.apply_removal_policy(RemovalPolicy.DESTROY)

        # Creating Lambda Function for DynamoDB
        DB_Lambda = self.create_lambda("Saqlain_DB_Lambda","./Resources","DBApp.lambda_handler",lambda_role)

        # Defining a rule to convert my lambda into cronjob 
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_events/Schedule.html
        rule = events.Rule(self, "WHApp_Event_Rule",
            schedule=events.Schedule.rate(Duration.minutes(60)),

            # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_events_targets/LambdaFunction.html
            targets=[targets.LambdaFunction(handler=WHApp_Lambda)])
        rule.apply_removal_policy(RemovalPolicy.DESTROY)

        """ Create SNS topic and subscriptions"""
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns/Topic.html
        topic = sns.Topic(self,"WHApp_Lambda")
        """ Subscription for sns topic"""
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns_subscriptions/EmailSubscription.html
        topic.add_subscription(subscriptions.EmailSubscription("saqlain.mushtaque.skipq@gmail.com"))

        # For 4 websites 8 metrices are created, 4 for Availability and 4 for latency
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch/Metric.html

        for i in range(len(constant.URLs_Monitor)):
            # For Availability
            dimension = {'URL': constant.URLs_Monitor[i]}
            availability_metrics = cw.Metric(
                metric_name = constant.Availability_Metric,
                namespace = constant.Namespace,
                dimensions_map = dimension)

            # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch/Alarm.html  
            availability_alarm = cw.Alarm(self, f"{constant.URLs_Monitor[i]}_Availability_Errors",
                metric=availability_metrics,
                evaluation_periods=60,
                threshold=1,
                comparison_operator=cw.ComparisonOperator.LESS_THAN_THRESHOLD)
            # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch_actions/SnsAction.html
            availability_alarm.add_alarm_action(cw_actions.SnsAction(topic))
            

            # For Latency
            dimension = {'URL': constant.URLs_Monitor[i]}
            latency_metrics = cw.Metric(
                metric_name = constant.Latency_Metric,
                namespace = constant.Namespace,
                dimensions_map = dimension)
                
            # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch/Alarm.html  
            latency_alarm = cw.Alarm(self, f"{constant.URLs_Monitor[i]}_Latency_Errors",
                metric=latency_metrics,
                evaluation_periods=60,
                threshold=0.5,
                comparison_operator=cw.ComparisonOperator.GREATER_THAN_THRESHOLD)
            # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch_actions/SnsAction.html
            latency_alarm.add_alarm_action(cw_actions.SnsAction(topic))

        """creating Table"""
        dbTable = self.creat_DynamoDBTable()
        dbTable.grant_read_write_data(DB_Lambda)
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html#aws_cdk.aws_lambda.Function.add_environment
        DB_Lambda.add_environment("Saqlain_Table",dbTable.table_name)
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns_subscriptions/LambdaSubscription.html
        topic.add_subscription(subscriptions.LambdaSubscription(DB_Lambda))

    def create_lambda(self,id,asset,handler,role):
        return lambda_.Function(self,
            id = id,
            code=lambda_.Code.from_asset(asset),
            handler=handler,
            # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Runtime.html#aws_cdk.aws_lambda.Runtime
            runtime=lambda_.Runtime.PYTHON_3_9,
            timeout = Duration.minutes(5),
            role = role )

    # create Lambda Role
    # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_iam/Role.html    
    def create_lambda_role(self):
        lambdaRole = iam_.Role(self, "Lambda_role",
            assumed_by=iam_.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                #iam_.ManagedPolicy.from_aws_managed_policy_name("Service/cloudformation.amazonaws.com"),
                iam_.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess")
            ])
        return lambdaRole

    # Function for creat_DYnamoDB Table
    # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_dynamodb/Table.html
    
    def creat_DynamoDBTable(self):
        table = db.Table(self,"Saqlain_Table",
            partition_key=db.Attribute(name="id", type=db.AttributeType.STRING),
            sort_key = db.Attribute(name="timestamp", type=db.AttributeType.STRING),
            removal_policy = RemovalPolicy.DESTROY,
        )
        return table