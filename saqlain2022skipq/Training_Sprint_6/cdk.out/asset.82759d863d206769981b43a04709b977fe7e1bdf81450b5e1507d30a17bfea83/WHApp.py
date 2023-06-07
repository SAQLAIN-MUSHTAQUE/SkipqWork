import urllib3
import datetime
import constants as constant
from CloudWatchData import AWSCloudWatch
import Links
import os

def lambda_handler(event,context):
    table = os.environ['Saqlain_CRUD_Table']
    URLs_Monitor = Links.get_link(f"{table}")
    if URLs_Monitor == None:
        URLs_Monitor = []
    else: 
        URLs_Monitor
    values = {}

    i = 0
    while i < len(URLs_Monitor):

        # Getting Availability value either "0" or "1"
        availablity = getavail(URLs_Monitor[i])

        # Getting Latency value in second
        latency = getlat(URLs_Monitor[i])

        values.update({f"{URLs_Monitor[i]}":f"Availablity = {availablity}  ||  Latency = {latency}"})

        # dimension
        dimensions = [{'Name': 'URL','Value': URLs_Monitor[i]}]
        
        # Sending Data to cloud watch
        # for Availability
        AWSCloudWatch().cwmd(constant.Namespace,constant.Availability_Metric,dimensions,availablity)
        #for latency
        AWSCloudWatch().cwmd(constant.Namespace,constant.Latency_Metric,dimensions,latency)

        i += 1
    return values

def getavail(url):
   http = urllib3.PoolManager()
   response = http.request('GET',url)
   # return the availability
   if response.status == 200:
       return 1.0
   else:
       return 0.0
   

def getlat(url):
   http = urllib3.PoolManager()
   start = datetime.datetime.now()
   response = http.request('GET', url) 
   end = datetime.datetime.now()
   delta = end - start           # to get the consume time
   latencySec = round(delta.microseconds * .000001, 6)
   # return the latency 
   return latencySec