import boto3
import os 
import gzip
import base64
import json


sns = boto3.client('sns', region_name = "us-east-2")
user_arn = os.environ["UserArn"]
Admin_arn = os.environ["AdminArn"]

def process_event(event): 
    # Parse event by decoding, decompressing
    decoded_payload = base64.b64decode(event.get("awslogs").get("data"))
    uncompressed_payload = gzip.decompress(decoded_payload)
    payload = json.loads(uncompressed_payload)
    return payload


def lambda_handler(event,context):
    payload = process_event(event)
    
    logGroup = payload.get("logGroup")
    logStream = payload.get("logStream")
    logEvents = payload.get("logEvents")
    lambda_function_name = payload.get("logGroup").split("/")[-1]
    msg = [levent["message"] for levent in logEvents]
    
    
    # Initialize an empty dictionary
    result = {}
    
    # Loop over each line
    for line in msg:
        # Split the line into key-value pairs using the ':' separator
        pairs = line.split(':')
        # Add the key-value pair to the dictionary
        result[pairs[0]] = pairs[1]


    # Pre-Signed URL
    if 'https' in result:
        pre_signed = 'https:'+result['https']
    else: 
        pre_signed = ""
        
    # Take out latest Report from msg
    for x in msg:
        if x.startswith('REPORT RequestId'):
            REPORT = x
            break
        
    # make every element of Report in dictionary
    Report = {}
    for pair in REPORT.strip().split('\t'):
        key, value = pair.split(': ')
        Report[key] = value

    print(Report)
    
    # Request ID
    RequestID = Report['REPORT RequestId'] if 'REPORT RequestId' in Report else  ""
    
    # Duration
    Duration = Report['Duration'] if 'Duration' in Report else ""
    
    # Billed Duration
    bill_Dur = Report['Billed Duration'] if 'Billed Duration' in Report else ""
    
    # Total Memory sized
    t_memo = Report['Memory Size'] if 'Memory Size' in Report else ""
    
    # Used Memory sized
    u_memo = Report['Max Memory Used'] if 'Max Memory Used' in Report else ""
    
    
    user_email_body = f"""
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    
    
      Lambda function details
      Lambda function name ::: {lambda_function_name}
      Log Group ::: {logGroup}
      Log Stream ::: {logStream}
      RequestID ::: {RequestID} 
      Pre Signed URL ::: {pre_signed}
      Billed Duration ::: {bill_Dur} ms
      Memory Used ::: {u_memo} MB
      Max Memory Size ::: {t_memo} MB
     
     
     
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    """
    
    Admin_email_body = f"""
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    
    
      Lambda function  details
      Lambda function name ::: {lambda_function_name}
      Log Group ::: {logGroup}
      Log Stream ::: {logStream}
      RequestID ::: {RequestID} 
      Billed Duration ::: {bill_Dur} ms
      Max Memory ::: {t_memo} MB
      Memory Used ::: {u_memo} MB
     
     
     
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    """

    
    # For User:
    sns.publish(TopicArn=user_arn, Message= user_email_body, Subject = "Pre-Signed URL and report")
    
    # For Admin:
    sns.publish(TopicArn=Admin_arn, Message= Admin_email_body, Subject = "URL report")

    
    return (f"log_group={logGroup} \n" , f"log_stream = {logStream}\n", f"lambda = {lambda_function_name} \n", f"msg = {msg} \n",
            f"Pre Signed URL = {pre_signed} \n" , f"Report = {Report} \n" ,f"Request ID = {RequestID} \n", f"Duration = {Duration} \n",
            f"Billed Duration = {bill_Dur} \n", f"Max Memory Size = {t_memo} \n", f"Used Memory = {u_memo} \n",
        )
