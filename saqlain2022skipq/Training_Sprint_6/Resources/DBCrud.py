import boto3
import os
import json

db_crud = boto3.resource('dynamodb', region_name='us-east-2')
db_CRUD_name_table = os.environ['Saqlain_CRUD_Table']
table = db_crud.Table(db_CRUD_name_table)

def lambda_handler(event,context):

    if event["httpMethod"] == "GET":
    # Perform a scan operation on the table to retrieve all items
        response = table.scan()
        items = response['Items']
        
        return {
            'statusCode': 200,  
            'body': json.dumps(items)
        }

    #  ******** POST ********
    elif event["httpMethod"] == "POST":
        body = json.loads(event['body'])
        item = {
            'id': body['id'],
            'URL': body['URL']
        }
        table.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': json.dumps("item has been added") 
        }

    # Single item    
    elif event["httpMethod"] == "GET" and event['queryStringParameters']:
        
        id = event["queryStringParameters"]["id"]
        response = table.get_item(Key={'id': id})
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps('Item not found')
            }
        return {
            'statusCode': 200,
            'body': json.dumps(response['Item'])
        }


    # To update
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/update_item.html
    elif event["httpMethod"] == "PUT":
        body = json.loads(event['body'])
        id = body['id']
        url = body['URL']
        
        response = table.update_item(
                Key={
                    'id': id,
                },
                UpdateExpression='SET #updateUrl = :URL',
                ExpressionAttributeValues={
                    ':URL': url
                },
                ExpressionAttributeNames={
                    '#updateUrl': 'URL'
                },
                ReturnValues='UPDATED_NEW'
            )
        
        return {
            'statusCode': 200,
            'body': json.dumps(f'ID {id} updated successfully to {url}')
        }

    # To delete item:
    elif event["httpMethod"] == "DELETE" and event['queryStringParameters']:
        id = event['queryStringParameters']["id"]
        response = table.delete_item(Key={'id': id})
        return {
            'statusCode': 200,
            'body': json.dumps('Item deleted from DynamoDB table')
        }
        

    #  ******** If Nothing run ********
    else:
        return {
            'statusCode': 405,
            'body': json.dumps('Method not allowed')
        }