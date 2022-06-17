
# Welcome to  CDK Python project!

This is a `Cloud9`  project for `Python Lambda Function` development with CDK.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python Lambda Function project. This is build on Cloud9 environment
with use of `EC2` instance , and lambda function.
The initialization process of this project start with version checking and upgrade of python version.


To manually : check and upgrade version , must be higer than `3.0` 
```
$ python --version       
$ python vim ~/.bashrc               //opens a editor ,then scroll down, and press `i` to insert
 alias python='/usr/bin/python3'    // after this , press `esc` button , and type `:wq` to write and quit the editor
$ soucre ~/.bashrc                  // to apply changes immediatley in `bash` file , type this  
```
Also check and update amazon CLI version
```
$ aws --version                     // To check version
$ curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"  -o "awscliv2.zip
$ unzip awscliv2.zip
$ sudo ./aws/install                //Done with Upgrade
$ rm awscliv2.zip                 // It will delete the zip file which was download from above link
```
To intialization process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth         //if after that an error  occurs, then run this `$ .venv/bin/pip3.6 install -r requirements.txt` then again `cdk synth`
```
and finally deploy on Lambda Console or(To convert into Cloud Formation Template) type below command:
```
$ cdk deploy                    // also u can run cdk synth and cdk deploy combine ,type: $ cdk synth && cdk deploy. 
```
Happy Coding!!!


To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.


## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation


Enjoy !!!
