import json
import boto3
import dotenv
from dotenv import load_dotenv
import os

load_dotenv()

TABLE_NAME=os.getenv("TABLE_NAME")


def lambda_handler(event, context):
    
    # Convert event(body) to python dict
    data = json.loads(event['body'])
    
    # Initialize dynamodb boto3 object
    dynamodb = boto3.resource('dynamodb')
    
    # Set dynamodb table name variable
    ddbTableName = TABLE_NAME
    table = dynamodb.Table(ddbTableName)

    # Write the content to ddb database
    table.put_item(Item=data)

    # Create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(data)
    }

    return response