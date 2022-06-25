import boto3


class cloud_watch:
    def __init__(self):
        self.client = boto3.client('cloudwatch')
    
    def publish_metric(self,nameSpace,metricName,dimension,value):                  # UDF for publishsing  
        response = self.client.put_metric_data(Namespace=nameSpace,         
        MetricData=[{
            'MetricName':metricName,
            'Dimensions':dimension,
            'Value':value
    }]

    )        
            
