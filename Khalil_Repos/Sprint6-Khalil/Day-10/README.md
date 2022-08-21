
# Welcome to your AWS Design and Development Python project!

This is a `Design Day 10` Task .



Task to do for this Project is:

1) Design & Develop - A customer sends a request to an API Gateway endpoint. He wants a PDF report
to be generated in return. The problem is the max response time of API Gateway is 30 seconds. The
API Gateway is configured with a Lambda function that is responsible for performing the process of
generating PDF reports. Imagine, the customer wants a report of a huge chunk of data and the
processing time that the lambda will take can exceed 5 mins.  The API Gateway processing time is less 
than what the lambda function will take to perform the pdf generation process.
How we can manage to generate PDF report without making the API Gateway crash. How would you
tackle such a problem?

### The Methods to Tackle this problem are;
```
1. Fix it  by Try to increase your lambda function size, the processing time will be increase.
2. Use lambdaInvoke() function which is part of the "aws-sdk". With lambdaInvoke() instead of going through APIGateway 
    you can directly call that function. But this is useful on server side only.
3. The best method to tackle this is -> Make request to APIGateway -> Inside the function push the received data into an 
    SQS Queue -> Immediately return the response -> Have a lambda function ready which triggers when data available in 
    this SQS Queue -> Inside this triggered function do your actual time complex executions -> Save the data to a data 
    store -> If call is comes from client side(browser/mobile app) then implement long-polling to get the final processed result from the same data store.

Now since api is immediately returning the response after pushing data to SQS, your main function execution time will be much less now, and will 
resolve the APIGateway timeout issue.

4. Short polling : In this scenario the client requests data from the server. If the data is not available, the server sends an ‘empty’ response. 
                    When the client receives the response, it requests the data again from the server immediately or after a predefined delay. These request - response 
                    cycles go on until the data is available on the server and sent back to the client.

5. Long polling : This is an improved version of the short polling scenario explained above. In this scenario the server does not immediately return a response 
                    but waits until the data is available or a timeout would be near. Depending on the situation the response could include the data or not. When 
                    the client receives a response without data, it would sent a new request (immediately or after a predefined delay). If the response contains data, the process would stop.

6. Server-Sent Events (SSE) : Server-Sent Events is a server push technology enabling a client to receive automatic updates from a server over an HTTP connection. 
                            After the connection is established the server can send events to the client until the client closes the connection.
7. WebSocket: The WebSocket protocol provides full-duplex communication channels over a single TCP connection. After the initial handshake, it allows for two way 
            data transfer between client and server, and this with lower overhead than polling alternatives.
            Applied to our use case the client would first setup a WebSocket connection to the server. Once the connection is established it sends a request for the 
            report to be generated. The server on its turn would generate the report and only when the generation finishes send back the report download URL as a response, using the same connection.

```

### The AWS Resources will be used, listed as:

```
1) API GateWay
2) Lambda
3) DynamoDB (Optional)

```
#### References
- [Amazon API gateway timeout; stackoverflow]('wwwhttps://stackoverflow.com/questions/31973388/amazon-api-gateway-timeout')

- [How to overcome API Gateway timeouts using WebSocket]('https://medium.com/hatchsoftware/how-to-overcome-api-gateway-timeouts-using-websocket-86d946fabb93')

Happy Coding!!!
