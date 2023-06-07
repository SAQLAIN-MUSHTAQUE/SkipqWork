def lambda_handler(event, context):
    #print(event)
    return 'I am {} from {} cohort, Have a nice day you all!'.format(event['name'],event['cohort'])