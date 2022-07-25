import aws_cdk as cdk
from aws_cdk import(
 Stage
)

from constructs import Construct
from sprint4_khalil.sprint4_khalil_stack import Sprint4KhalilStack


class StageStack(Stage):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        self.stage= Sprint4KhalilStack(self, "Sprint4KhalilStack")
        
        
        


