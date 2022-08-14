
# Welcome to your AWS Design and Development Python project!

This is a `Design Day 5` Task .



Task to do for this Project is:

1) How would you automate deployment (e-g on AWS) for a system that has:

```
1) Source code in a repo;

--> Basically, this is an initial step of any method of automated deployment like we used CI/CD deployment, So  Before any creation of 
artifact first code will be pushed into any repo, then the, for deployment the code will be fetched from the repo and an artifact will be generated into S3.  

2) How do we generate an artifact from the repo that gets published and later is used in some services?

--> As we previously use CI/CD suit for automating deployment, in which as source code pushed on Repo, we call ShellStep() method for the build
so here basically it automatically generates an artifact in S3 and fetched form S3 for CodeBuild.
but if we generate artifact manually then we will first use `class aws_cdk.aws_codebuild.Artifacts() ` for build output  and  
`class aws_cdk.aws_codepipeline.Artifact()` for fetch the artifact from S3.

3) Are there more than one solutions?

--> Yes, we have an alternative for Code Deploy, that is Jenkins. So it's upon the developer that, if he uses only  AWS-Resources then he can go with
CI/CD suit(code build/code pipeline/code deploy). If not, then he can go for Jenkins.

--> Reasons to use Jenkins or CI/CD: https://devops.stackexchange.com/questions/6863/what-is-better-between-jenkins-aws-codedeploy-for-ci-cd


==> Resources: 
------------- What is an artifact in DevOps: https://jfrog.com/knowledge-base/what-is-a-software-artifact/#:~:text=A%20DevOps%20artifact%20is%20a,layout%20depending%20on%20the%20technology.


```

Happy Coding!!!
