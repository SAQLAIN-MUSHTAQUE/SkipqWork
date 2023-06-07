import json

def handler(event, context):
    print  ("request {}",format(json.dumps(event)))

    return{
        'statuscode':200,
        'headers': {
            'content-Type':'text/plain'
        },
        'body': 'Hello, CDK! You have hit {}\n'.format(event['path'])
    }