import boto3
import os

def lambda_handler(event,context):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/index.html
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

    # https://docs.python.org/3/library/os.html#os.environ
    db_name = os.environ['Saqlain_Table']
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/index.html
    table = dynamodb.Table(db_name)
    
    # https://dheeraj3choudhary.com/crud-operations-for-aws-dynamodb-using-python-boto3-script
    record = event['Records'][0]['Sns']
    
    table.put_item(
        Item = {
            'id' : record['MessageId'],
            'timestamp' : record['Timestamp'],
            'subject' : record['Message']
            
        },
        
    )
