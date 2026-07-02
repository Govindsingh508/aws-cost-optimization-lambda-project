# Technical Documentation

## Project Objective

The objective of this project is to identify AWS resources that generate unnecessary costs and automatically notify administrators through an email report.

The project scans AWS resources, collects optimization recommendations, and sends a formatted report using Amazon SNS.

---

# Lambda Execution Flow

The Lambda function performs the following steps:

1. Starts Lambda execution.
2. Creates AWS service clients.
3. Fetches AWS Compute Optimizer recommendations.
4. Scans EC2 resources.
5. Identifies:
   - Unattached EBS Volumes
   - Unused Elastic IPs
   - User-created Snapshots
6. Generates a formatted cost optimization report.
7. Sends the report through Amazon SNS.
8. Returns the execution summary.

---

# AWS Services Used

### AWS Lambda
Runs the Python code without managing any servers.

### Amazon EC2
Retrieves information about EBS volumes, Elastic IPs, and snapshots.

### AWS Compute Optimizer
Identifies idle AWS resources and estimates possible monthly cost savings.

### Amazon SNS
Sends the generated report to the configured email address.

---

# IAM Permissions Used

The Lambda execution role requires the following permissions:

- AmazonEC2ReadOnlyAccess
- ComputeOptimizerReadOnlyAccess
- AmazonSNSFullAccess

---

# Future Improvements

Possible enhancements include:

- Automatic deletion of unused resources after approval.
- Cost Explorer integration.
- Multi-region scanning.
- CSV/PDF report generation.
- S3 report storage.
- Slack or Microsoft Teams notifications.

---

# Learning Outcomes

This project demonstrates practical experience with:

- AWS Lambda
- Amazon EC2 APIs
- AWS Compute Optimizer
- Amazon SNS
- IAM Roles and Permissions
- Python (Boto3)
- AWS Cost Optimization
- Serverless Architecture
