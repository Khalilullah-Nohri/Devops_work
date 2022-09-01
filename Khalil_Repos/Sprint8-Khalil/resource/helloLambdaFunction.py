

def lambda_handler(event, context):
    # User define lambda function
    return "ehlan w sehaln {} {}!".format(event['first_name'],event['cohort_name'])   # first task , to print Hello World