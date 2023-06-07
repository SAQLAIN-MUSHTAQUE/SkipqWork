# Welcome to Design and Develop Problem 6!

## **Topics**:
+ ## [Prerequisite](#prerequisites) 
+ ## [Use commands](#useful-commands).
+ ## [**(a.) Design and Develop Problem 6**](#design-and-develop-problem-6)
  - ### [Question of Design Problem](#question-of-design-problem)
  - ### [Problem Design](#problem-design-1)
  - ### [Creating Lambda Function](#creating-lambda)
  - ### [Creating SNS](#creating-sns-topics-and-subscription)
  - ### [Trigger CloudWatch log](#trigger-from-cloudwatch-logs-group)
  - ### [Application](#creating-application)


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

# **Design and Develop problem 6 :**

## **Question of Design Problem :**
 Client needs a Notification System – that notifies the Admins about report summaries, users about operations within the system, and notifies clients/users about any changes. What AWS service(s) would you use for such a system?

## **Problem Design :**
 The structural design of Design Problem 6 is given below:  
 ![Alt text](ScreenShot/Design%206.jpg)  

## **Creating Lambda :**

 First create Lambda function in Stack file:
 ```
 from aws_cdk import (
    Stack,
    aws_lambda as lambda_,)

 from constructs import Construct

 class DesignProblem6Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_role = self.create_lambda_role()

        fn = self.create_lambda("SaqlainDesign6","./Resources","Application.lambda_handler",lambda_role)

    # Creating Lambda 
    def create_lambda(self, id, asset, handler, role):
        return lambda_.Function(self, 
        id = id,
        code= lambda_.Code.from_asset(asset),
        handler = handler,
        runtime=lambda_.Runtime.PYTHON_3_9,
        role = role 
        )

    # create Lambda Role 
    def create_lambda_role(self):
        
 ```  

 The "Resources" where handler file is situated and "Application.py" is a file name.  

 After creating lambda function, assign a Removal policy to it:
 ```
 from aws_cdk import RemovalPolicy,

    fn.apply_removal_policy(RemovalPolicy.DESTROY)
 ```

 Also I have IAM Role definition to give full permission to **Cloudwatch** and **SNS**.
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
                iam_.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess")
            ])
        
        return lambdaRole
 ```

 ## **Creating SNS Topics And Subscription :**  
 In this Design we assign 2 topics and subscriptions, one for Admin and other one for user:

 ```
 from aws_cdk import (
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,

 )  

        # SNS Topic

        # User Topic
        user_topic = sns.Topic(self,"user")

        # Subscription for user topic
        user_topic.add_subscription(subscriptions.EmailSubscription("USER_EMAIL"))

        # getting topic.arn
        user_arn = user_topic.topic_arn
        fn.add_environment("UserArn",user_arn)

        # Admin Topic
        Admin_topic = sns.Topic(self,"Admin")

        # Subscription for Admin topic
        Admin_topic.add_subscription(subscriptions.EmailSubscription("ADMIN-USER"))

        # getting topic.arn
        Admin_arn = Admin_topic.topic_arn
        fn.add_environment("AdminArn",Admin_arn)
 ```  


## **Trigger from CloudWatch logs group :**
 ```
 from aws_cdk import (
    aws_logs as logs,
    aws_logs_destinations as destinations,

 )

        # Grant permissions to the Lambda function to read logs
        log_group = logs.LogGroup.from_log_group_arn(
            self, 'LogGroup', log_group_arn='arn:aws:logs:us-east-2:31***********:log-group:/aws/lambda/SaqlainDesignProblem7Stac-SaqlainPayloadapp12BF556-Zu4bdSBrSMyp:*'
        )

        # CloudWatch Logs subscription filter   
        logs.SubscriptionFilter(self, "LogFilter",
            log_group=log_group,
            destination=destinations.LambdaDestination(fn),
            filter_pattern=logs.FilterPattern.all_terms(),
        )

        log_group.grant_read(fn)
 ```

## **Creating Application :**
 ```
 import boto3
 import os 
 import gzip
 import base64
 import json
 import logging

 log = boto3.client("logs", region_name = "us-east-2")
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

    # Pre-Signed URL
    if msg[1][0:5] == "https":
        pre_signed = msg[1][:-1]
    elif msg[1][:8] == '[ERROR]':
        pre_signed = msg[1][:-1]
    else: 
        pre_signed = ""
        
    
    
    Report = msg[3]
    Report = Report.split()
    
    RequestID = ""
    Duration = ""
    bill_Dur = ""
    t_memo = ""
    u_memo = ""

    
    # Request ID
    if 'RequestId:' in Report:
        RequestID = Report[(Report.index('RequestId:')) + 1]
    
    # Duration
    if "Duration:" in Report:
        Duration = Report[(Report.index('Duration:')) + 1]
    
    # Billed Duration
    if "Duration:" in Report:
        bill_Dur = Report[(Report.index('Duration:',(Report.index('Duration:')) + 1)) + 1]
    
    # Total Memory sized
    if 'Size:' in Report:
        t_memo = Report[(Report.index('Size:')) + 1]
    
    # Used Memory sized
    if 'Used:' in Report:
        u_memo = Report[(Report.index('Used:')) + 1]
    
    
    user_email_body = f"""
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    
    
      Lambda function Error details
      Lambda function name ::: {lambda_function_name}
      Log Group ::: {logGroup}
      Log Stream ::: {logStream}
      RequestID ::: {RequestID} 
      Pre Signed URL ::: {pre_signed}
      Billed Duration ::: {bill_Dur}
      Memory Used ::: {u_memo}
      Max Memory Size ::: {t_memo}
     
     
     
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    """
    
    Admin_email_body = f"""
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    
    
      Lambda function Error details
      Lambda function name ::: {lambda_function_name}
      Log Group ::: {logGroup}
      Log Stream ::: {logStream}
      RequestID ::: {RequestID} 
      Billed Duration ::: {bill_Dur}
      Max Memory ::: {t_memo}
      Memory Used ::: {u_memo}
     
     
     
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    """

    
    # For User:
    sns.publish(TopicArn=user_arn, Message= user_email_body, Subject = "Pre-Signed URL and report")
    
    # For Admin:
    sns.publish(TopicArn=Admin_arn, Message= Admin_email_body, Subject = "URL report")

    
    return (f"log_group={logGroup} \n" , f"log_stream = {logStream}\n", f"lambda = {lambda_function_name} \n", f"msg = {msg} \n",
            f"Pre Signed URL = {pre_signed} \n" , f"Report = {Report} \n" ,f"Request ID = {RequestID} \n", f"Duration = {Duration} ms \n",
            f"Billed Duration = {bill_Dur} ms \n", f"Max Memory Size = {t_memo} MB \n", f"Used Memory = {u_memo} MB \n",
        )

 ```
 