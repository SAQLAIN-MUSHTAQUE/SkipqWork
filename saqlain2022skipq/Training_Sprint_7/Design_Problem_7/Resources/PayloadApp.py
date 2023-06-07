import boto3
import os
import json

s3 = boto3.client('s3')
bucket = os.environ['SaqlainPayloadBucket']

def lambda_handler(event, context):

    if event["httpMethod"] == "GET":
        # ********* Generate the pre-signed URL for the file upload *********

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/generate_presigned_url.html
        file_name = event['queryStringParameters']['name']
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': bucket,
                'Key': file_name,
            },
            ExpiresIn=3600,
        )

        return {
            'statusCode': 200,
            'body': json.dumps(presigned_url)
        }

    else:
        return {
            'statusCode': 405,
            'body': json.dumps('Method not allowed')
        }