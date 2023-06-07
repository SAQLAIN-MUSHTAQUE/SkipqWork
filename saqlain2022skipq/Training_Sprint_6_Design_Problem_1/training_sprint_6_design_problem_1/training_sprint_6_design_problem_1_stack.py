from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    RemovalPolicy,
    aws_iam as iam_,
    aws_cloudwatch as cw,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_cloudwatch_actions as cw_actions,
 )
from constructs import Construct

class TrainingSprint6DesignProblem1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_iam/IRole.html#aws_cdk.aws_iam.IRole
        lambda_role = self.create_lambda_role()

        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
        API_Lambda = self.create_lambda("DesignAPI","./Resources","APIapp.lambda_handler",lambda_role)
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
        API_Lambda.apply_removal_policy(RemovalPolicy.DESTROY)


        # *********** Creating API ***********
         # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/RestApi.html
        api = apigateway.RestApi(self, "saqlain_api_design_problem",
            rest_api_name = "SaqlainAPIDesignProblem",
            endpoint_types=[apigateway.EndpointType.REGIONAL])
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_apigateway/README.html#openapi-definition
        all_resource = api.root.add_resource("arg1")

        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/LambdaIntegration.html
        api_handler = apigateway.LambdaIntegration(API_Lambda)
        
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/Resource.html#aws_cdk.aws_apigateway.Resource.add_method
        all_resource.add_method("POST", api_handler)

        # # Calling Metric
        # # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch/Metric.html
        arg1_metric = cw.Metric(
            metric_name = "arg1_metric",
            namespace = "SaqlainDesignProblem1",
            dimensions_map= {"arg1": "arg1_Demo"},
            period = Duration.seconds(10)
            )
        
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch/Alarm.html  
        arg1_alarm = cw.Alarm(self, "SaqlainDesignAlarm",
            metric= arg1_metric,
            evaluation_periods= 1,
            threshold=10,
            comparison_operator=cw.ComparisonOperator.GREATER_THAN_THRESHOLD)


        # SNS Alarm
        """ Create SNS topic and subscriptions"""
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns/Topic.html
        topic = sns.Topic(self,"Saqlian_API_Lambda")
        
        """ Subscription for sns topic"""
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns_subscriptions/EmailSubscription.html
        topic.add_subscription(subscriptions.EmailSubscription("saqlain.mushtaque.skipq@gmail.com"))

        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch_actions/SnsAction.html
        arg1_alarm.add_alarm_action(cw_actions.SnsAction(topic))

    # create Lambda Role
    # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_iam/Role.html    
    def create_lambda_role(self):
        
        lambdaRole = iam_.Role(self, "Lambda_role",
            assumed_by=iam_.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                #iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonAPIGatewayInvokeFullAccess"),
                iam_.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),

            ])
        return lambdaRole    

    # Creating Lambda 
    def create_lambda(self, id, asset, handler, role):
        return lambda_.Function(self, 
        id = id,
        code= lambda_.Code.from_asset(asset),
        handler = handler,
        runtime=lambda_.Runtime.PYTHON_3_9,
        role = role 
        )


