# Architecture Documentation

## Overview

This project uses a fully serverless architecture to automate AWS cost optimization.

Amazon EventBridge triggers the AWS Lambda function based on a scheduled rule. The Lambda function scans AWS resources, retrieves optimization recommendations, generates a cost optimization report, and sends it through Amazon SNS.

---

## Architecture Flow

1. Amazon EventBridge triggers the Lambda function on a schedule.
2. AWS Lambda scans Amazon EC2 resources.
3. Lambda retrieves idle resource recommendations from AWS Compute Optimizer.
4. Resource information is analyzed and a cost optimization report is generated.
5. Amazon SNS sends the report to the configured email address.

---

## AWS Services Used

- Amazon EventBridge
- AWS Lambda
- Amazon EC2
- AWS Compute Optimizer
- Amazon SNS
- IAM

---

## Benefits

- Fully serverless architecture
- Automated scheduled execution
- Low operational cost
- Easy to scale
- Minimal manual intervention
