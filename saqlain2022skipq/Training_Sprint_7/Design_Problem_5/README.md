# Welcome to Design and Develop Problem 5!

## **Topics**:
+ ## [Prerequisite](#prerequisites) 
+ ## [Use commands](#useful-commands).
+ ## [**(a.) Design and Develop Problem 5**](#design-and-develop-problem-5)
  - ### [Question of Design Problem 5](#question-of-design-problem)
  - ### [Problem Design](#problem-design-5)
  - ### [Creating Lambda Function](#creating-lambda)
  - ### [Creating S3 Bucket](#creating-amazon-s3-bucket)
  - ### [SNS and Email Subscription](#creating-sns-topic-and-assign-subscription)
  - ### [Creating Application](#application)


## **Prerequisites :**

The `cdk.json` file tells the CDK Toolkit how I execute my app.

The initialization process creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in my path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can check the installation of NVM and NPM installation:
#### **Step:1**
```
$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
```
#### **Step:2**
After running the above commands, it's time to add a variable to your bash command. Normally, it was located from these file paths:
```
$ nano ~/.bash_profile
```
Then paste the code below, then hit crtl + o + enter then ctrl + x to close the file.
```
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
```
Then source ~/.bash_profile to set up environment for NVM:
```
$ source ~/.bash_profile
```
#### **Step:3**
To check the available lists of available node version that you can use. Type this command.
```
$ nvm ls-remote
```
NVM can install any of these versions available in the list. For example, to install version v16.3.0, type:
```
nvm install v16.3.0 && nvm use v16.3.0 && nvm alias default v16.3.0
```
Then install aws cdk module:
```
$ npm install -g aws-cdk
```
After that install all the dependencies:
```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

# **Design and Develop problem 5 :**

## **Question of Design Problem :**
*Suppose there are 10 files uploading to S3 bucket each day. For each file received on cloud storage, you have a mechanism to process the file. During the processing, your code parses the text and counts the number of times each word is repeated in the file. For example, in the following text: “Hello World and Hello There”, your code should be able to say that "hello" has been used twice, "world" has occurred once and so on. Then it will store the results in some storage and email to some email address after successful processing.*





## **Problem Design :**
The structural design of Design Problem 5 is given below:  

![Alt text](ScreenShot/Design%20Problem.drawio.png)

  
## **Creating Lambda :**

First create Lambda function in Stack file:
```
from aws_cdk import (
    Stack,
    aws_lambda as lambda_,)

from constructs import Construct

class TrainingSprint6DesignProblem1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

       fn = self.create_lambda("Saqlain_Event_APIs","./Resources","Application.lambda_handler",lambda_role,)

        # Creating Lambda 
            def create_lambda(self, id, asset, handler, role):
                return lambda_.Function(self, 
                id = id,
                code= lambda_.Code.from_asset(asset),
                handler = handler,
                runtime=lambda_.Runtime.PYTHON_3_9,
                role = role 
                )
```
The "Resources" where handler file is situated and "S3App.py" is a file name.  

After creating lambda function, assign a Removal policy to it:
```
 from aws_cdk import RemovalPolicy,

    API_Lambda.apply_removal_policy(RemovalPolicy.DESTROY)
```

Also I have IAM Role definition for to give full permission to  **"service-role/AWSLambdaBasicExecutionRole"**, **"AmazonSNSFullAccess"** and Full access to **"AmazonS3FullAccess"**:
```
from aws_cdk import aws_iam as iam_
    lambda_role = self.create_lambda_role()

# creating Lambda Role:-
def create_lambda_role(self):   
    lambdaRole = iam_.Role(self, "Lambda_role",
        assumed_by=iam_.ServicePrincipal("lambda.amazonaws.com"),
        managed_policies=[
            iam_.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
            iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonSNSFullAccess"),
            iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
        ])
    return lambdaRole
```
  
## **Creating Amazon S3 Bucket :**

 After that create a S3 bucket so the user can upload the 10 files every day and he will get the  result of the recent files that uploaded.
 ```
 From aws_cdk import aws_s3 as s3

 # Create an S3 bucket to receive the files

        bucket = s3.Bucket(self, "Bucket",
                            removal_policy=RemovalPolicy.DESTROY,
                            block_public_access=s3.BlockPublicAccess(block_public_policy=False)
                        )
        fn.add_environment("NAME_OF_BUCKET",bucket.bucket_name)

        # Grant S3 permission to trigger the Lambda function
        bucket.grant_read(fn)

        
        # Set up an S3 bucket notification to invoke the Lambda function
        fn.add_event_source(S3EventSource(bucket,
            events=[s3.EventType.OBJECT_CREATED],
            filters=[s3.NotificationKeyFilter(prefix="data/")]
        ))
```
  
## **Creating SNS Topic And Assign Subscription :**  
 Creating a sns topics and assign an email so the word counts can be send on that:
 ```
 From aws_cdk import (
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
 )
        topic = sns.Topic(self, "SaqlainTopic")
        # topic.add_subscription(subscriptions.LambdaSubscription(fn))
        topic.add_subscription(subscriptions.EmailSubscription("saqlain.mushtaque.skipq@gmail.com"))

        # getting topic.arn
        arn = topic.topic_arn 
        fn.add_environment("TopicArn",arn)

 ```

## **Application :**
 The Application for this service is given below:

  ```
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
    objects = sorted(objects, key=lambda x: x['LastModified'], reverse=True)[:10] # get the 10 most recent objects
    
    
    keys = []
    for i in range(len(objects)-1):
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
            tstr+= f"{word:<0} : {count:>0}\n"
        table_str += tstr
        
        space ="\n"+" "*20+"\n"
        table_str+= space
            
    print (table_str)
    
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
  ```




