# AWS Cost Optimization using AWS Lambda

## Project Overview

This project automatically identifies AWS resources that may be generating unnecessary costs and sends a detailed cost optimization report via Amazon SNS.

The solution is built using AWS Lambda and integrates with multiple AWS services to help identify:

- Unattached EBS Volumes
- Unused Elastic IP Addresses
- User Snapshots
- AWS Compute Optimizer Idle Resource Recommendations

The generated report is delivered through email using Amazon SNS.

## Features

- Detects unattached EBS volumes
- Detects unused Elastic IP addresses
- Lists user-owned EBS snapshots
- Fetches AWS Compute Optimizer idle resource recommendations
- Calculates potential monthly savings
- Generates a structured cost optimization report
- Sends email notifications using Amazon SNS
- Displays AWS Region and execution time in the report
- Includes clear recommendations for each detected resource

## Architecture

The project follows a simple serverless architecture

```text
EC2 Resources
      │
      ▼
AWS Lambda
      │
      ├── EC2 API
      ├── Compute Optimizer API
      ├── EBS Snapshots
      └── Elastic IPs
      │
      ▼
Amazon SNS
      │
      ▼
Email Notification
```

## AWS Services Used

| Service | Purpose |
|----------|----------|
| AWS Lambda | Runs the automation script |
| Amazon EC2 | Fetches EBS volumes, snapshots and Elastic IPs |
| AWS Compute Optimizer | Detects idle resources and estimated savings |
| Amazon SNS | Sends the cost optimization report through email |
| IAM | Provides secure permissions for Lambda |


## Project Workflow

1. AWS Lambda is triggered manually or on a schedule using Amazon EventBridge.
2. Lambda scans the AWS account for:
   - Unattached EBS Volumes
   - Unused Elastic IP Addresses
   - User-owned Snapshots
3. Lambda fetches idle resource recommendations from AWS Compute Optimizer.
4. Resource details and estimated savings are collected.
5. A structured cost optimization report is generated.
6. Amazon SNS sends the report to the configured email address.
7. The user reviews the report and removes unused resources to reduce AWS costs.


