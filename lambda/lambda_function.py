# Import required AWS SDK and date/time libraries
import boto3
from datetime import datetime
from zoneinfo import ZoneInfo

# Main Lambda function to fetch AWS resource details and send cost optimization report via SNS
def lambda_handler(event, context):

    print("======== Lambda Execution Started =======")

# Create aws service clients
    ec2 = boto3.client('ec2')

    sns = boto3.client('sns')

    optimizer = boto3.client('compute-optimizer')

    region = ec2.meta.region_name

    execution_time = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%d-%b-%Y %I:%M:%S %P %Z")

   # Fetch AWS Compute Optimizer recommendations
    print("====Fetching AWS Compute Optimizer recommendations====")

    response = optimizer.get_idle_recommendations()

# Storecompute optimizer recommendations in a list
    optimizer_recommendations = []

    print(response)

    # Extract useful recommendations details

    for recommendation in response['idleRecommendations']:

        optimizer_recommendations.append({

            'ResourceId': recommendation['resourceId'],

            'ResourceType': recommendation['resourceType'],

            'Finding': recommendation['finding'],

            'Description': recommendation['findingDescription'],

            'Savings': recommendation['savingsOpportunity']['estimatedMonthlySavings']['value'],

            'Currency': recommendation['savingsOpportunity']['estimatedMonthlySavings']['currency'],

            'SavingsPercentage': recommendation['savingsOpportunity']['savingsOpportunityPercentage']

})

# Fetch details of ec2 resources
    print("==== Scanning EC2 Resources ====")

    volumes = ec2.describe_volumes()
    
    addresses = ec2.describe_addresses()

    snapshots = ec2.describe_snapshots(OwnerIds=['self'])

# List used to store detected resources
    unattached_volumes = []

    unused_eips = []

    user_snapshots = []
    
    #Find unattached volumes  

    for volume in volumes['Volumes']:

        print(volume)

        if len(volume['Attachments']) == 0:

            unattached_volumes.append({
                'VolumeId': volume['VolumeId'],
                'size': volume['Size'],
                'state' : volume['State'],
                'availablezone': volume['AvailabilityZone']
            })
    
    # Find unused elastic IPs

    for address in addresses['Addresses']:

          if 'AssociationId' not in address:

            unused_eips.append({
                'PublicIp': address['PublicIp']
            })

# Collect user snapshots
    for snapshot in snapshots['Snapshots']:
        
         user_snapshots.append({
           'SnapshotId': snapshot['SnapshotId'],
            'VolumeSize': snapshot['VolumeSize']
         })

    print("Unattached Volumes:")

    for vol in unattached_volumes:
        print(vol)

    print("Unused Elastic IPs:")

    for eip in unused_eips:
        print(eip)
    
    print("user Snapshots:")
       
    for snap in user_snapshots:
         print(snap)

    print("optimizer_recommendations:")

    for recommendation in optimizer_recommendations:
        print(recommendation)
    
# Build the email report only if resources or recommendations exist

    print("===== Publishing Cost Optimization Report Via SNS =====")

    if unattached_volumes or unused_eips or user_snapshots or optimizer_recommendations:

        message = "=========================================\n"
        message += "      AWS COST OPTIMIZATION REPORT\n"
        message += "=========================================\n\n"

        message += f"Region : {region}\n\n"
        message += f"Execution Time : {execution_time}\n\n"

        message += "SUMMARY\n"
        message += "-----------------------------------------\n"

        message += f"Unattached EBS Volumes     : {len(unattached_volumes)}\n"
        message += f"Unused Elastic IPs         : {len(unused_eips)}\n"
        message += f"EBS Snapshots              : {len(user_snapshots)}\n"
        message += f"Compute Optimizer Findings : {len(optimizer_recommendations)}\n\n"

        if unattached_volumes:

            message += "-----------------------------------------\n"
            message += "UNATTACHED EBS VOLUMES\n"
            message += "-----------------------------------------\n\n"

            for vol in unattached_volumes:

                message += (
                f"Volume ID: {vol['VolumeId']}\n"
                f"Size: {vol['size']} GB\n"
                f"State: {vol['state']}\n"
                f"Availability Zone: {vol['availablezone']}\n\n"
                )

        if unused_eips:

            message += "-----------------------------------------\n"
            message += "UNUSED ELASTIC IPs \n"
            message += "-----------------------------------------\n\n"

            for eip in unused_eips:

                message += (
                f"Public IP: {eip['PublicIp']}\n\n"
                )

        if user_snapshots:

            message += "-----------------------------------------\n"
            message += "SNAPSHOTS\n"
            message += "-----------------------------------------\n\n"

            for snap in user_snapshots:

                message += (
                f"Snapshot ID: {snap['SnapshotId']}\n"
                f"Volume Size: {snap['VolumeSize']} GB\n\n"
                )

        if optimizer_recommendations:

            message += "-----------------------------------------\n"
            message += "AWS COMPUTE OPTIMIZER\n"
            message += "-----------------------------------------\n\n"

            for recommendation in optimizer_recommendations:

                message += (
                f"Resource ID: {recommendation['ResourceId']}\n"
                f"Resource Type: {recommendation['ResourceType']}\n"
                f"Finding: {recommendation['Finding']}\n"
                f"Description: {recommendation['Description']}\n"
                f"Estimated Monthly Savings: {recommendation['Savings']:.2f} {recommendation['Currency']}\n"
                f"Savings Percentage: {recommendation['SavingsPercentage']:.0f}%\n\n"
                )

        message += (
            "-----------------------------------------\n"
            "RECOMMENDATIONS\n"
            "-----------------------------------------\n"
            "--> Review unattached EBS volumes before deleting.\n"
            "--> Release unused Elastic IPs.\n"
            "--> Remove unnecessary snapshots after verification.\n"
            "--> Review AWS Compute Optimizer recommendations before taking action.\n\n"
        )

        message += "=========================================\n"
        message += "Generated by AWS Cost Optimization Lambda\n"
        message += "=========================================\n"

    # Send email report via Amazon SNS
        sns.publish(
            TopicArn='arn:aws:sns:eu-north-1:151498473865:Cost-optimization-alerts',
            Subject='AWS Cost Optimization Report',
            Message=message
        )

    print("===== SNS notification sent successfully =====")
    print("===== Lambda Execution Completed====")

# Return execution summary
    return {
        'statusCode': 200,
        'body':{
             "Unattached Volumes":  unattached_volumes,
             "unusedElasticIPS": unused_eips,
             "userSnapshots": user_snapshots,
             "optimizerRecommendations": optimizer_recommendations
        }
    }
