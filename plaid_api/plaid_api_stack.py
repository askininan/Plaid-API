from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    RemovalPolicy,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_apigateway as apigw
)


class PlaidApiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Deploy dynamoDB table
        table_ddb = dynamodb.Table(
            self, 
            id="plaid_content_table",
            removal_policy=RemovalPolicy.DESTROY,
            partition_key=dynamodb.Attribute(
                name="id", 
                type=dynamodb.AttributeType.STRING
            )
        )


        # Deploy post_handler lambda function
        post_function = lambda_.Function(
            self, 
            id="post_handler",
            code=lambda_.Code.from_asset("./post_handler"),
            handler="post_handler.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
        )

        # Grant permission to post_funtion to write ddb table
        table_ddb.grant(post_function, "dynamodb:PutItem")


        # Deploy APIGW
        api = apigw.RestApi(self, 
            "Plaid-API",  
        )

        #Create post resource in APIGW
        post_apiResource = api.root.add_resource("post_apiResource")

        #Post_handler lambda function and APIGW integration
        post_content_integration = apigw.LambdaIntegration(post_function)
        post_apiResource.add_method("POST", post_content_integration)
