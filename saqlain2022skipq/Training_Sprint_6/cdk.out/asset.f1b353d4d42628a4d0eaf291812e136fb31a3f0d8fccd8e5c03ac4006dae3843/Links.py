import boto3
import botocore.exceptions

def get_link(table):
    client = boto3.client('dynamodb', region_name="us-east-2")

    try:
        data = client.scan(TableName=table, AttributesToGet=['URL'])
        item = data['Items']
        URLs_Monitor = []

        for i in range(len(item)):
            URLs_Monitor.append(item[i]['URL']['S'])

        return URLs_Monitor
    except botocore.exceptions.ClientError as e:
        print("Error: {}".format(e))