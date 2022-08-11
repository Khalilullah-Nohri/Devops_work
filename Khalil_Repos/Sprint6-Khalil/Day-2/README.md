
# Welcome to your CDK Python project!

This is a `Design and Development Day 2` Project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

Task to do for this Project is:
1) Design and Develop:    Consider that you are getting events in the format [{“event1”:{“attr1”: value }}] from different APIs.
    a) How will you parse the event to get the value?
    b) How will you return 10 latest events when required?

So For this , I create two `Lambda RestApi` and two  httpMethod `POST` and `GET` along with this, also create a `lambda Function` and `dynamodb` table in main Stack File,
further, create another .py lambda file , in which a user define POST and GET function are created and inside that `get_item` and `put-item` function 
has also been called to put Data into DyNamoDB table. .

and Finally 


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
