#!/usr/bin/env python3
import os

import aws_cdk as cdk

from sprint2_khalil.sprint2_khalil_stack import Sprint2KhalilStack


app = cdk.App()

# https://docs.aws.amazon.com/cdk/v2/guide/tagging.html
# Tags are informational key-value elements that you can add to constructs in your AWS CDK app. A tag applied to a given construct also applies to all of its taggable children
cdk.Tags.of(app).add("cohort" , "Pegasus")
cdk.Tags.of(app).add("name" , "Khalilullah")

Sprint2KhalilStack(app, "Sprint2KhalilStack",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=cdk.Environment(account='123456789012', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()
