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
