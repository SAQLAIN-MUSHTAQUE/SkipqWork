#!/usr/bin/env python3

import aws_cdk as cdk

from workshop_practice.workshop_practice_stack import WorkshopPracticeStack


app = cdk.App()
WorkshopPracticeStack(app, "workshop-practice")

app.synth()
