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
    aws_codedeploy as codedeploy,
    aws_apigateway as apigateway,

)

from constructs import Construct
from Resources import constants as constant
from Resources import Links as link
import os

class TrainingSprint5Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_iam/IRole.html#aws_cdk.aws_iam.IRole
        lambda_role = self.create_lambda_role()

        """Section For Lambda Function"""
        #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
        WHApp_Lambda = self.create_lambda("Saqlain_WHL_App","./Resources","WHApp.lambda_handler",lambda_role,)
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
        WHApp_Lambda.apply_removal_policy(RemovalPolicy.DESTROY)

        # Creating Lambda Function for DynamoDB
        DB_Lambda = self.create_lambda("Saqlain_DB_Lambda","./Resources","DBApp.lambda_handler",lambda_role,)


        ''' ********** SPRINT 5 API CRUD ********** '''
        # Creating Lambda Function for DynamoDB CRUD
        DB_Crud_Lambda = self.create_lambda("Saqlain_DB_CRUD_Lambda","./Resources","DBCrud.lambda_handler",lambda_role,)

        """Build a public CRUD API Gateway endpoint """
        dbCrud = self.creat_DynamoDbCRUDTable()
        dbCrud.grant_read_write_data(DB_Crud_Lambda)
        dbCrud.grant_read_write_data(WHApp_Lambda)

        DB_Crud_Lambda.add_environment("Saqlain_CRUD_Table",dbCrud.table_name)
        WHApp_Lambda.add_environment("Saqlain_CRUD_Table",dbCrud.table_name)

        """ Adding API """
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/RestApi.html
        api = apigateway.RestApi(self, "saqlain_api",
            rest_api_name = "SaqlainAPI",
            endpoint_types=[apigateway.EndpointType.REGIONAL])
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_apigateway/README.html#openapi-definition
        all_resource = api.root.add_resource("URLs")

        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/LambdaIntegration.html
        crud_handler = apigateway.LambdaIntegration(DB_Crud_Lambda)
        
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/Resource.html#aws_cdk.aws_apigateway.Resource.add_method
        all_resource.add_method("GET", crud_handler)
        all_resource.add_method("POST", crud_handler)
        all_resource.add_method("PUT", crud_handler)
        all_resource.add_method("DELETE", crud_handler)

        
        ''' ********** SPRINT 4 Metrices for Web Crawler ********** '''
        ''' Obtain AWS Lambda Metrics: '''
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
        dimension = {'FunctionName':WHApp_Lambda.function_name}
        # duration Metric
        duration_metrics = WHApp_Lambda.metric("Duration")
        # Invocations Metric
        ConcurrentExecutions_metric = WHApp_Lambda.metric("ConcurrentExecutions")
        # Async Event Age
        AsyncEventAge_metric = WHApp_Lambda.metric("AsyncEventAge")

        ''' Create alarm On metrics'''
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch/Alarm.html
        # Duration Alarm  
        duration_alarm = cw.Alarm(self, "DurationError",
            metric= duration_metrics,
            evaluation_periods=60,
            threshold=850,
            comparison_operator=cw.ComparisonOperator.GREATER_THAN_THRESHOLD)
        
        # ConcurrentExecutions Alarm 
        ConcurrentExecutions_alarm = cw.Alarm(self, "ConcurrentExecutionsExceed",
            metric=ConcurrentExecutions_metric,
            evaluation_periods=60,
            threshold=1,
            comparison_operator=cw.ComparisonOperator.GREATER_THAN_THRESHOLD)
        
        # AsyncEventAge Alarm
        AsyncEventAge_alarm = cw.Alarm(self, "AsyncEventAgeExceed",
            metric= AsyncEventAge_metric,
            evaluation_periods=60,
            threshold=30,
            comparison_operator=cw.ComparisonOperator.GREATER_THAN_THRESHOLD)
        
        ''' ******* Deployement Group ******* '''
        # ****** Alias ******
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Alias.html#aws_cdk.aws_lambda.Alias
        # used to make sure each CDK synthesis produces a different Version
        version = WHApp_Lambda.current_version
        alias = lambda_.Alias(self, "Saqlain_Alias",
                alias_name="Prod",
                version=version
            )
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_codedeploy/LambdaDeploymentGroup.html
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Alias.html#aws_cdk.aws_lambda.Alias
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_codedeploy/LambdaDeploymentConfig.html
        deployment_group = codedeploy.LambdaDeploymentGroup(self, "SaqlainDeploymentGroup",
            #application=WHApp_Lambda,
            alias=alias,
            alarms = [duration_alarm, ConcurrentExecutions_alarm, AsyncEventAge_alarm],
            #auto_rollback=codedeploy.AutoRollbackConfig(deployment_in_alarm=True),
            deployment_config = codedeploy.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE
        )

        '''Defining a rule to convert my lambda into cronjob '''
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

        """creating Table"""
        dbTable = self.creat_DynamoDBTable()
        dbTable.grant_read_write_data(DB_Lambda)
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html#aws_cdk.aws_lambda.Function.add_environment
        DB_Lambda.add_environment("Saqlain_Table",dbTable.table_name)
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns_subscriptions/LambdaSubscription.html
        topic.add_subscription(subscriptions.LambdaSubscription(DB_Lambda))

       
        # For 4 websites 8 metrices are created, 4 for Availability and 4 for latency
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch/Metric.html
        
        URLs_Monitor = link.get_link(f"{dbCrud}")
        if URLs_Monitor == None:
            URLs_Monitor = []
        else: 
            URLs_Monitor

        for i in range(len(URLs_Monitor)):
            # For Availability
            dimension = {'URL': URLs_Monitor[i]}
            availability_metrics = cw.Metric(
                metric_name = constant.Availability_Metric,
                namespace = constant.Namespace,
                dimensions_map = dimension)

            # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch/Alarm.html  
            availability_alarm = cw.Alarm(self, f"{URLs_Monitor[i]}_Availability_Errors",
                metric=availability_metrics,
                evaluation_periods=60,
                threshold=1,
                comparison_operator=cw.ComparisonOperator.LESS_THAN_THRESHOLD)
            # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch_actions/SnsAction.html
            availability_alarm.add_alarm_action(cw_actions.SnsAction(topic))
            

            # For Latency
            dimension = {'URL': URLs_Monitor[i]}
            latency_metrics = cw.Metric(
                metric_name = constant.Latency_Metric,
                namespace = constant.Namespace,
                dimensions_map = dimension)
                
            # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch/Alarm.html  
            latency_alarm = cw.Alarm(self, f"{URLs_Monitor[i]}_Latency_Errors",
                metric=latency_metrics,
                evaluation_periods=60,
                threshold=0.5,
                comparison_operator=cw.ComparisonOperator.GREATER_THAN_THRESHOLD)
            # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch_actions/SnsAction.html
            latency_alarm.add_alarm_action(cw_actions.SnsAction(topic))

    def create_lambda(self,id,asset,handler,role,):
        return lambda_.Function(self,
            id = id,
            code=lambda_.Code.from_asset(asset),
            handler=handler,
            # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Runtime.html#aws_cdk.aws_lambda.Runtime
            runtime=lambda_.Runtime.PYTHON_3_9,
            timeout = Duration.minutes(5),
            role = role,)

    # create Lambda Role
    # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_iam/Role.html    
    def create_lambda_role(self):
        
        lambdaRole = iam_.Role(self, "Lambda_role",
            assumed_by=iam_.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                #iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonAPIGatewayInvokeFullAccess"),
                iam_.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"),
                iam_.ManagedPolicy.from_aws_managed_policy_name('AWSCodeBuildAdminAccess'),
            ])
        return lambdaRole


    # Function for creat_DynamoDB Table
    # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_dynamodb/Table.html
    def creat_DynamoDBTable(self):
        table = db.Table(self,"Saqlain_Table",
            partition_key=db.Attribute(name="id", type=db.AttributeType.STRING),
            sort_key = db.Attribute(name="timestamp", type=db.AttributeType.STRING),
            removal_policy = RemovalPolicy.DESTROY,
        )
        return table

    # Function for creat_DynamoDB CRUD URLs Table
    def creat_DynamoDbCRUDTable(self):
        table = db.Table(self,"Saqlain_CRUD_Table",
            partition_key=db.Attribute(name="id", type=db.AttributeType.STRING),
            removal_policy = RemovalPolicy.DESTROY,
        )
        return table