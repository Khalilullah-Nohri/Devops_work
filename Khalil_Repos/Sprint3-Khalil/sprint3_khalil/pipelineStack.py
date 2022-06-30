import aws_cdk as cdk
from aws_cdk import(
    Stack,
    pipelines as pipe,
    aws_codepipeline_actions as pipeactions,
    aws_iam as iam_
)
from constructs import Construct


# from sprint3_khalil.stageStack import StageStack
from  sprint3_khalil.stageStack import StageStack
class PipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        
        # pipelineRoles_ = self.createGroupRole()    # if role will use for synth ,then use CodeBuildStep(), and it's last argument is role

        
                    # 1st stage for CI/CD --> Source
        # For CodePipeline : https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/CodePipelineSource.html 
        # For GitHubTrigger: https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_codepipeline_actions/GitHubTrigger.html#aws_cdk.aws_codepipeline_actions.GitHubTrigger.POLL
        # For Secret Value : https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.core/SecretValue.html#aws_cdk.core.SecretValue
        source=pipe.CodePipelineSource.git_hub("Khalilullah2022SkipQ/Pegasus_Python_SkipQ", 
                                        authentication =cdk.SecretValue.secrets_manager('khalil-git-hub-oauth-token'),branch="main",
                                        trigger=pipeactions.GitHubTrigger('POLL')     # POLL : CodePipeline periodically checks the source for changes.
        )
        # source=pipe.CodePipelineSource.connection("Khalilullah2022SkipQ/Pegasus_Python_SkipQ", 
        #                                 authentication =cdk.SecretValue.secrets_manager('khalil-github-oauth-token'),branch="main",
        #                                 trigger=pipeactions.GitHubTrigger('POLL')
        # )
        
                    # Time to build , 2nd stage of CI/CD
        # For ShellStep:  https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/ShellStep.html
        synth=pipe.ShellStep("Synth",input=source,
        commands=["cd Khalil_Repos/Sprint3-Khalil/","pip install -r requirements.txt","npm install -g aws-cdk","cdk synth"],
        primary_output_directory="Khalil_Repos/Sprint3-Khalil/cdk.out"  #, role=pipelineRoles_
        )
        
                    # uses CodePipeline to deploy CDK apps.
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/CodePipeline.html
        modern_pipeline = pipe.CodePipeline(self, "Pipeline",synth=synth)
        
                
        betaStage=StageStack(self, "Stage-Beta"       )
        prodStage=StageStack(self, "Stage-Production" )
        
                # Unit testing
        unitTesting =pipe.ShellStep("Unit Testing",
        commands=["cd Khalil_Repos/Sprint3-Khalil/","pip install -r requirements-dev.txt","pip install pytest","npm install -g aws-cdk","pytest"]
        )
        
        #  add Beta and production stages to pipeline
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/CodePipeline.html
        # Fro post: https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/Step.html#aws_cdk.pipelines.Step
        modern_pipeline.add_stage(betaStage ,pre=[unitTesting])
        modern_pipeline.add_stage(prodStage ,pre = [pipe.ManualApprovalStep("Prior to Stage")]) # pre= Additional steps to run before any of the stacks in the stage. 
        
        
        
    # def createGroupRole(self):
    #     role=iam_.Role(self,"pipeline-role",
    #     assumed_by=iam_.CompositePrincipal(
    #             iam_.ServicePrincipal('codebuild.amazonaws.com'),
    #             iam_.ServicePrincipal("lambda.amazonaws.com"),
    #             iam_.ServicePrincipal("sns.amazonaws.com")
    #             ),
    #         managed_policies=[
    #             iam_.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
    #             iam_.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
    #             iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"),
    #             iam_.ManagedPolicy.from_aws_managed_policy_name("AwsCloudFormationFullAccess"),
    #             iam_.ManagedPolicy.from_aws_managed_policy_name("AWSCodePipeline_FullAccess"),
    #             iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
    #         ]
    #     )
    #     return role