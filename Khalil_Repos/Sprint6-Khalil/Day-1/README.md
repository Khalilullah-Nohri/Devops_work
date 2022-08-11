
# Welcome to your CDK Python project!

This is a `Design and Development Day 1` Project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

Task to do for this Project is:
1) Design and Develop:    Consider that you are getting an event response as {“arg1”: 10} from an API.
    a) Make an AWS app that generates an alarm if arg1 > 10.
    b) When the alarm is raised, sends an email to a dummy account.

So For this , I create a `Lambda RestApi` and `POST` httpMethod along with this, also create a `lambda Function` in main Stack File,
further, create another .py lambda file , in which a user define POST function is created and inside that `put_metric_data` function has 
also been called to put metrics on CLoud watch. SNS Topic also being used in stack to notify the user.

and Finally 

2) What will you do if there is no lambda invocation even though the code is working fine and there is no error generated?
    ```
    https://docs.aws.amazon.com/lambda/latest/dg/troubleshooting-invocation.html
    1. General: Cannot invoke function with other accounts or services, Issue: You can invoke your function directly, but it doesn't run when another service or account invokes it.
    2. add_permission() method of Lambda function
    3. Cron() schedule problem
    
    ```

To Run the Project:

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
