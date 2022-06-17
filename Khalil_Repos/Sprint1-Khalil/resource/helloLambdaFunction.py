

def lambda_handler(event, context):
    return "Ahlan wa sehlan {} {}!".format(event['first_name'],event['cohort_name'])   # first task , to print Hello World