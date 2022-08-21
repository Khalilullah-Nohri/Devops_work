
# Welcome to your AWS Design and Development Python project!

This is a `Design Day 11` Task .



Task to do for this Project is:

1) Design & Develop - What if we have 15MB file that we have to upload on S3 using API gateway. We
have the limitation that our API gateway has the maximum payload capacity of 10MB. How you will
solve this problem?

### The specific solution to Tackle this problem is;
```
The user makes an API, which is served by API Gateway and backed by a Lambda function. 
The Lambda function computes a signed URL granting upload access to an S3 bucket and returns that to API Gateway, 
and API Gateway forwards the signed URL back to the user. 
At this point, the user can use the existing S3 API to upload files larger than 10MB.

```

### The AWS Resources will be used, listed as:

```
1) API GateWay
2) Lambda
3) S3

```
#### References
- [Uploading Large Payloads through API Gateway]('https://sookocheff.com/post/api/uploading-large-payloads-through-api-gateway/#:~:text=API%20Gateway%20supports%20a%20reasonable,to%20an%20API%20Gateway%20request.')

- [Using pre-signed URLs to upload a file to a private S3 bucket]('https://sanderknape.com/2017/08/using-pre-signed-urls-upload-file-private-s3-bucket/')
- [Boto3 PreSignedURL Documentation]('https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html')
Happy Coding!!!
