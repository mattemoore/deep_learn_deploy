import boto3
import base64
import uuid
from time import sleep

# Setup AWS objects:
#  Create IAM User Group w/ programmatic access
#    Attach 'AmazonEC2FullAccess' and AWSCodeDeployFullAccess' policies to group
#  Create IAM User w/ programmatic access
#    Add created User to created User Group
#  Create AWS Code Deploy Application e.g. 'DeepLearningApplication'
#    Attach Deployment Group that uses EC2 instances with tag 'Name:DeepLearningBox'
#  Create an AWS S3 Bucket e.g. 'deeplarningbucket1' w/ versioning enabled
#  (Optional for debugging) Create an AWS Security Group that allows SSH incoming connections named 'SSH'

# Setup deploy box:
#   Install Python 3.6 + Boto3 + awscli on box that will invoke deployment
#   Run 'aws configure' in Python dir and enter access keys for created User
#     Enter default region e.g 'us-east-1' and select 'json' as default output format

# AWS CodeDeploy application name
app_name = '<app_name>' 
# The tag specified in application's Deployment Group
app_deploy_group_tag = '<app_deploy_group_tag>'
# AWS S3 bucket (with versioning enabled) to store builds/output
app_bucket_name = '<bucket_name>'

ec2 = boto3.client('ec2')
region_name = ec2._client_config.region_name

print('Retrieving deep learning AMI image id for your region', region_name, '...')
image_filter = [{'Name': 'name',
                 'Values': ['Deep Learning AMI (Ubuntu) Version 2.0']}]
images = ec2.describe_images(Filters=image_filter)
image_id = images['Images'][0]['ImageId']
print('Retrieved image id', image_id)

print('Requesting deep learning spot instance from EC2...')
code_deploy_agent_bucket = 'aws-codedeploy-us-' + region_name
user_data = r'#!/bin/bash\n'\
            'apt-get -y update\n'\
            'apt-get -y install ruby\n'\
            'apt-get -y install wget\n'\
            'cd /home/ubuntu\n'\
            'wget https://{0}.s3.amazonaws.com/latest/install\n'\
            'chmod +x ./install\n'\
            './install auto\n'.format(code_deploy_agent_bucket)
user_data = base64.b64encode(user_data.encode()).decode('ascii')
launch_spec = {
    'InstanceType': 'p2.xlarge',
    'UserData': user_data,
    'ImageId': image_id
}
response = ec2.request_spot_instances(
    InstanceCount=1,
    LaunchSpecification=launch_spec,
)
request_id = response['SpotInstanceRequests'][0]['SpotInstanceRequestId']
print('Spot request received from EC2...waiting for fulfillment from EC2...')

while True:
    sleep(10)
    request_filter = [{'Name': 'spot-instance-request-id',
                       'Values': [request_id]}]
    response = ec2.describe_spot_instance_requests(Filters=request_filter)
    code = response['SpotInstanceRequests'][0]['Status']['Code']
    if code == 'fulfilled':
        instance_id = response['SpotInstanceRequests'][0]['InstanceId']
        break

print('Spot request fulfilled by EC2 via instance', instance_id)

# tag instance with app_deploy_name

# push build package to S3

# deploy to instance

# put output (logs, models etc.) into S3 bucket

# terminate instance (cancel spot request)

