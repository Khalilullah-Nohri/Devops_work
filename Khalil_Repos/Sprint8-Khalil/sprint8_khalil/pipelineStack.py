import aws_cdk as cdk
from aws_cdk import(
    Stack,
    pipelines as pipe,
    aws_codepipeline_actions as pipeactions,
    aws_iam as iam_,
    aws_codebuild as codebuild
)
from constructs import Construct



from  sprint8_khalil.stageStack import StageStack
class PipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        
                    # 1st stage for CI/CD --> Source
        source=pipe.CodePipelineSource.git_hub("Khalilullah2022SkipQ/Pegasus_Python_SkipQ", 
                                        authentication =cdk.SecretValue.secrets_manager('Khalil-gitHub-oauth-token'),branch="main",
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

        dokerBuild=pipe.CodeBuildStep("Docker-Build-Tests",commands=[],
            build_environment=codebuild.BuildEnvironment(
                # The user of a Docker image asset in the pipeline requires turning on
                # 'dockerEnabledForSelfMutation'.
                build_image=codebuild.LinuxBuildImage.from_asset(self, "Docker-Image",directory="./pyresttest").from_docker_registry(name="docker:dind"),
                privileged=True
            ),
            partial_build_spec=codebuild.BuildSpec.from_object({
                "version": 0.2,
                "phases":{
                  "install":{
                    "commands":[
                  "nohup /usr/local/bin/dockerd --host=unix:///var/run/docker.sock --host=tcp://127.0.0.1:2375 --storage-driver=overlay2 &"
                  "timeout 15 sh -c \"until docker info; do echo .; sleep 1; done\"" 
                    ]
                  },
                  "pre_build":{
                      "commands":["ls","cd Khalil_Repos/Sprint8-Khalil/pyresttest","docker build -t pyrest:PyRestTest ."
                      ]
                  },
                  "build":{
                      "commands":[
                          "docker images","docker run --rm pyrest:PyRestTest"
                          ]
                      
                  }
                }
            })
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

        modern_pipeline.add_stage(betaStage ,pre=[unitTesting],post=[dokerBuild])
        modern_pipeline.add_stage(prodStage ,pre = [pipe.ManualApprovalStep("Prior to Stage")]) # pre= Additional steps to run before any of the stacks in the stage. 
        
        