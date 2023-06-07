import boto3

def test_table():
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/index.html
    dynamodb = boto3.resource('dynamodb',region_name='us-east-2')

    try:
        table = dynamodb.Table('Alpha-SaqlainStage-SaqlainTable7141CC55-I66WOVF0TCM3')
        response = table.scan()
        data = response["Items"]

        return data
    
    except Exception as error:
        print ('Error occured: ',error)

test_table()
