import boto3

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html
class AWSCloudWatch:
    def __init__(self):
        self.client =  boto3.client('cloudwatch')
        
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/put_metric_data.html#    
    def cwmd(self, Namespace, MetricName, dimensions, value):                 # define cloudwatch metric data
        
        '''CloudWatch Data Template'''
        response = self.client.put_metric_data(
            Namespace = Namespace,
            MetricData=[
                {
                    'MetricName': MetricName,
                    'Dimensions': dimensions,
                    'Value': value
                },
            ]
        )