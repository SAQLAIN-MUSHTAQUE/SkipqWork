import boto3
import os
import re 


s3 = boto3.client('s3')
sns = boto3.client('sns')
arn = os.environ["TopicArn"]
bucket = os.environ["SaqlainBucket"]


def lambda_handler(event, context):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/list_objects_v2.html
    objects = s3.list_objects_v2(Bucket=bucket)['Contents']
    objects = sorted(objects, key=lambda x: x['LastModified'], reverse=True)[:11] # get the 10 most recent objects
    
    
    keys = []
    for i in range(len(objects)):
        if str(objects[i]["Key"][0:5]) == "data/":
            keys.append(objects[i]["Key"])
        
    table_str = ""   
    for k in range(len(keys)):
        Map = {}
        obj = s3.get_object(Bucket=bucket, Key=keys[k])
        data = obj['Body'].read().decode('utf-8')
        
        # split words and store them in a dictionary 
        # https://www.w3schools.com/python/python_regex.asp
        for word in re.findall(r'\b\w+\b', data):
            word = word.lower()
            if word in Map:
                Map[word] += 1
            else:
                Map[word] = 1
                
                
        # Convert dictictionary into table
        # Title
        tstr= " "*20+f"TEXT {k+1}"+" "*20+"\n"
        
        
        # Loop over the dictionary items and append the rows to the string
        for word, count in Map.items():
            tstr+= f"{word:} : {count:}\n"
        table_str += tstr
        
        space ="\n"+" "*20+"\n"
        table_str+= space
            
    # print (table_str)
    
        # {'Words':<10} is a string format specifier that is used to format the header of the table.
    
        # 'Words' is the string that we want to format, and < indicates that the string should be left-aligned within the available space. 10 specifies the width of the field, i.e., the total number of characters that the field should take up.
        
        # So, in this case, 'Words' is left-aligned within a field of width 10. The < is optional since left-alignment is the default behavior.
        
        # Similarly, {'Count':>10} is used to right-align the Count column in the table. > indicates that the string should be right-aligned within the available space, and 10 specifies the width of the field.
            
    # Storing Data
    result_content = table_str
    file_name ="result.txt"
        
    # uploading result file
    s3.put_object(Bucket=bucket, Key='results/' + file_name, Body=result_content, ContentType='text/plain')
    
    sns.publish(TopicArn=arn, Message=str(table_str), Subject = "Words count from files")
    
    
    return (table_str)