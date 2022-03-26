#!/usr/bin/env python3

import aws_cdk as cdk

from plaid_api.plaid_api_stack import PlaidApiStack


app = cdk.App()
PlaidApiStack(app, "plaid-api")

app.synth()
