import boto3
import os
import json
import datetime
from decimal import Decimal
from operator import itemgetter

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
db_table = os.environ['Saqlain_Event_Table']
table = dynamodb.Table(db_table)

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    if event["httpMethod"] == "POST":
        # Parse the request body
        request_body = json.loads(event["body"])
        
        # Extract the value from the request body
        value = request_body[0]["event1"]["attr1"]
        time = datetime.datetime.now()
        formatted_datetime = str(time.strftime("%Y-%m-%d %H:%M:%S"))
        id = event["requestContext"]["apiId"]
        
        # Create the response body
        item = {"id": id, "value": Decimal(value), "timestamp": formatted_datetime} 

        # put item in the table
        table.put_item(Item=item)
        
        # Create the response object
        response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(item, cls=DecimalEncoder)
        }
        
        return response

    elif event["httpMethod"] == "GET":
        list1 = []
        list2 = []
                
        response = table.scan()
        items = response["Items"]
        items = json.loads(json.dumps(items, cls=DecimalEncoder))
        
        # table into list
        for i in range(len(items)):
            val = items[i]
            val_list = list(val.values())
            list1.append(val_list)

        
        # sorting entries w.r.t timestamps    
        sort_list = sorted(list1,key=itemgetter(2),reverse = True)

        
        # select 10 entries
        if len(sort_list)>10:
            entries = sort_list[:10]
        else:
            entries = sort_list
            
        
        # enter entries in list   
        for j in entries:
            x = {"APIid":j[1],"Time":j[2],"Value":j[0]}
            list2.append(x)
            
        
        # For Print Table
        
        # Get the keys of the dictionary to use as column headers
        headers = list(list2[0].keys())
        
        # Find the maximum length of each column
        col_widths = [max(len(str(d[h])) for d in list2) for h in headers]
        
        # Print the headers
        for i, header in enumerate(headers):
            print(f"{header:<{col_widths[i]}}", end=" ")
        print()

        # Print the data
        for d in list2:
            for i, header in enumerate(headers):
                print(f"{d[header]:<{col_widths[i]}}", end=" ")
            print()
        
        
        # Create the response object
        response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(list2)
        }
        
        return response
    else:
        return {
            'statusCode': 405,
            'body': json.dumps('Method not allowed')
        }
