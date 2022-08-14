
# Welcome to your CDK Python project!

This is a `Design Day 4` Task .



Task to do for this Project is:
1) Design & Develop - Deploy, maintain and rollback pipeline for an artifact deployment e-g lambda package, docker image etc.

```

1) What do you think if the latest deployment is failing?
--> The main reason of latest deployment failing is that,  any of our alarms which we set in as a parameter in code deploy construct will cross its threshold. 

2)How will you rollback?
--> I can configure a deployment group or deployment to automatically roll back when a deployment fails or when a monitoring threshold you specify 
is met. In this case, the last known good version of an application revision is deployed. You configure automatic rollbacks when 
you create an application or create or update a deployment group. Deployments can be rolled back automatically or manually.


3) How do you reduce such failures so there is less need to rollback?
--> We can use cdk destroy and run again our code or we can change our alarms threshold so that no any rollback occurs.

```





Happy Coding!!!
