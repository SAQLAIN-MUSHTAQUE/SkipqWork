from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as lambda_,
    aws_iam as iam_,
    RemovalPolicy,
    aws_apigateway as apigateway,
    aws_dynamodb as db,
)
from constructs import Construct

class DesignProblem2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_iam/IRole.html#aws_cdk.aws_iam.IRole
        lambda_role = self.create_lambda_role()

        #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
        Event_lambda = self.create_lambda("Saqlain_Event_APIs","./Resources","Application.lambda_handler",lambda_role,)
        # Removal Policies:
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
        Event_lambda.apply_removal_policy(RemovalPolicy.DESTROY)

        # Building Table
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_dynamodb/README.html
        db_table = self.creat_DynamoDBTable()
        db_table.grant_read_write_data(Event_lambda)
        Event_lambda.add_environment("Saqlain_Event_Table",db_table.table_name)

        
        # Creating APIs
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/RestApi.html
        # 1st API   
        api1 = apigateway.RestApi(self, "saqlain_event_1",
            rest_api_name = "SaqlainEvent1",
            endpoint_types=[apigateway.EndpointType.REGIONAL])

        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/LambdaIntegration.html
        handler = apigateway.LambdaIntegration(Event_lambda)

        api1_resource = api1.root.add_resource("event1")
        api1_resource.add_method("GET",handler)
        api1_resource.add_method("POST",handler)
        
        # 2nd API   
        api2 = apigateway.RestApi(self, "saqlain_event_2",
            rest_api_name = "SaqlainEvent2",
            endpoint_types=[apigateway.EndpointType.REGIONAL])

        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/LambdaIntegration.html
        handler = apigateway.LambdaIntegration(Event_lambda)

        api2_resource = api2.root.add_resource("event2")
        api2_resource.add_method("GET",handler)
        api2_resource.add_method("POST",handler)


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
                iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonAPIGatewayInvokeFullAccess"),
                iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"),
            ])
        return lambdaRole

    def creat_DynamoDBTable(self):
        table = db.Table(self,"Saqlain_Event_Table",
            partition_key=db.Attribute(name="id", type=db.AttributeType.STRING),
            sort_key = db.Attribute(name="timestamp", type=db.AttributeType.STRING),
            removal_policy = RemovalPolicy.DESTROY,
        )
        return table
