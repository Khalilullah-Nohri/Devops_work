import datetime, urllib3            # datetime: use for Date and time in latency funtion, urllib3: use for PoolManager() 
import global_instance as gb        # To import our create global_instance , to call "URL_TO_MONITOR" list
from  cloudwatch import cloud_watch

def lambda_handler(event,context):     
    cw_obj=cloud_watch()
    value=dict()
    for i in gb.URL_TO_MONITOR:                 # loop to iterate each portal/web form the list
        avail,latency  =calc_availability(i),calc_latency(i) # availabiliy of my web &    # latency of my web
        value.update({"Availability of {} ".format(i):avail ,"Latency of {} ".format(i):latency})

        dimension=[{'Name':'URL','Value':i}]
        
            #publish the Availability metric
        availMetric=gb.availMetric + " : "+i
        cw_obj.publish_metric(nameSpace=gb.metricNamespace,metricName=availMetric,dimension=dimension,value=avail)
        
            #publish the latency metric
        latencyMetric=gb.latencyMetric + " : "+i
        cw_obj.publish_metric(nameSpace=gb.metricNamespace,metricName=latencyMetric,dimension=dimension,value=latency)

    print(value)
    return "Success"   # return all webs , availability and latency
    
def calc_availability(url):             #method to find availability 
    http=urllib3.PoolManager()              
    response =http.request("GET",url)               # availabilty of any web
    if response.status==200:
        return 1.0
    else:
        return 0

def calc_latency(url):                      #method to find latency
    http=urllib3.PoolManager()
    start=datetime.datetime.now()                       #start time , to find latency
    response =http.request("GET",url)
    end=datetime.datetime.now()                         #end time , to find latency
    delta=end-start
    latencySecond=round(delta.microseconds*0.000001,6)      
    return latencySecond                #return the latency which occur on web