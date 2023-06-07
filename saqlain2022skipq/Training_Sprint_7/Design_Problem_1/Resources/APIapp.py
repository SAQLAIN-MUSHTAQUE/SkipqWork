import json
import boto3


client = boto3.client("cloudwatch")

def lambda_handler(event,context):
    body = json.loads(event["body"])
    item = {
        "arg1" : body["arg1"]
    }
    value = int(body["arg1"])
    
    # Creating CloudWatch Metric
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/put_metric_data.html#
    client.put_metric_data(
            Namespace = "SaqlainDesignProblem1",
            MetricData=[
                {
                    'MetricName': "arg1_metric",
                    'Dimensions': [
                        {
                            'Name': 'arg1',
                            'Value': "arg1_Demo"
                        }
                    ],
                    'Value': value
                },
            ]
        )

    if value <= 10:
        return {
            'statusCode': 200,
            'body': json.dumps(f"The arg1 = {value} is under range")
                } 
    else:
        return {
            'statusCode': 200,
            'body': json.dumps(f"The arg1 = {value} breached range")
                }