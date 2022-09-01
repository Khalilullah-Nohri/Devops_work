import aws_cdk as cdk
from aws_cdk import(
    Stack,
    pipelines as pipe,
    aws_codepipeline_actions as pipeactions,
    aws_iam as iam_
)
from constructs import Construct



from  sprint8_khalil.stageStack import StageStack
class PipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        
                    # 1st stage for CI/CD --> Source
        source=pipe.CodePipelineSource.git_hub("Khalilullah2022SkipQ/Pegasus_Python_SkipQ", 
                                        authentication =cdk.SecretValue.secrets_manager('Khalil-GitHub-Oauth-token'),branch="main",
                                        trigger=pipeactions.GitHubTrigger('POLL')     # POLL : CodePipeline periodically checks the source for changes.
        ) 
                    # Help of connection Method 
        # source=pipe.CodePipelineSource.connection("Khalilullah2022SkipQ/Pegasus_Python_SkipQ", 
        #                                 authentication =cdk.SecretValue.secrets_manager('khalil-github-oauth-token'),branch="main",
        #                                 trigger=pipeactions.GitHubTrigger('POLL')
        # )
        
                    # Time to build , 2nd stage of CI/CD
        synth=pipe.ShellStep("Synth",input=source,
        commands=["cd Khalil_Repos/Sprint8-Khalil/","pip install -r requirements.txt","npm install -g aws-cdk","cdk synth"],
        primary_output_directory="Khalil_Repos/Sprint8-Khalil/cdk.out"  #, role=pipelineRoles_
        )
        
                    # uses CodePipeline to deploy CDK apps.
        modern_pipeline = pipe.CodePipeline(self, "Pipeline",synth=synth)
        
                
        betaStage=StageStack(self, "Stage-Beta"       )
        prodStage=StageStack(self, "Stage-Production" )
        
                # Unit testing
        unitTesting =pipe.ShellStep("Unit Testing",
        commands=["cd Khalil_Repos/Sprint8-Khalil/","pip install -r requirements-dev.txt","npm install -g aws-cdk","pip install pytest","pytest"]
        )
        
        #  add Beta and production stages to pipeline

        modern_pipeline.add_stage(betaStage ,pre=[unitTesting])
        modern_pipeline.add_stage(prodStage ,pre = [pipe.ManualApprovalStep("Prior to Stage")]) # pre= Additional steps to run before any of the stacks in the stage. 
        
        