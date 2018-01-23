import base64
import sys
from time import sleep
import boto3

# Setup code: 
# Put contents of deploy code into root of code folder
# Ensure name of DL script to run on EC2 is in the root folder
# Name this script 'build_model.py'

# Setup deploy box:
# Install Python 3.6 + Boto3 + awscli (using pip) on box that will invoke deployment (dev box, CI box)
# Run 'aws configure' in Python dir and enter access keys for created User
# Enter default region e.g 'us-east-1' and select 'json' as default output

# Setup AWS resources (in default region):
# Create IAM User Group w/ programmatic access named 'DeployUserGroup'
# Attach 'AmazonEC2FullAccess' and 'AWSCodeDeployFullAccess' policies to 'DeployUserGroup'
# Create IAM User w/ programmatic access named 'DeployUser' and add to 'DeployUserGroup'
# Create a IAM Role named 'CodeDeployRole' that includes the 'AWSCodeDeployRole' and 'AmazonS3FullAccess' policies
# Create AWS CodeDeploy Application w/ name 'DeepLearningApplication'
# Create a Deployment Group named 'DeepLearningDeployGroup' that uses EC2 instances with tag 'Name:DeepLearningBox' and Service Role 'AWSCodeDeployRole'.
# Ensure that 'DeepLearningDeployGroup' is attached to 'DeepLearningApplication'
# Partially create a CodeDeploy Deployment w/ repository type Github, complete connection GitHub then cancel 
# (Optional for debugging) Create an AWS Security Group that allows SSH incoming connections w/ name 'SSH'


APP_NAME = 'DeepLearningApplication'
DEPLOY_TAG = ['Name', 'DeepLearningBox']
# AWS S3 bucket (with versioning enabled) to store output
app_bucket_name = '<bucket_name>'
DEEP_LEARN_AMI = 'Deep Learning AMI (Ubuntu) Version 2.0'
DEEP_LEARN_INSTANCE_TYPE = 'p2.xlarge'

print('Hello. Starting deploy...')

# Connect to EC2
ec2 = boto3.client('ec2')
region_name = ec2._client_config.region_name

# Requst deep learning Spot Instance
print('Retrieving deep learning', '"' + DEEP_LEARN_AMI + '"',
      '"AMI id for region', region_name + '...')
image_filter = [{'Name': 'name',
                 'Values': [DEEP_LEARN_AMI]}]
images = ec2.describe_images(Filters=image_filter)
image_id = images['Images'][0]['ImageId']
print('Success - Retrieved AMI id', image_id)

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
    'InstanceType': DEEP_LEARN_INSTANCE_TYPE,
    'UserData': user_data,
    'ImageId': image_id
}

response = ec2.request_spot_instances(
    InstanceCount=1,
    LaunchSpecification=launch_spec,
)

request_id = response['SpotInstanceRequests'][0]['SpotInstanceRequestId']
print('Success - Spot request', request_id,
      'created by EC2...\nWaiting for fulfillment from EC2...')


# Wait for Spot Instance Request fulfullment
request_filter = [{'Name': 'spot-instance-request-id', 'Values': [request_id]}]
while True:
    sleep(10)
    response = ec2.describe_spot_instance_requests(Filters=request_filter)
    code = response['SpotInstanceRequests'][0]['Status']['Code']
    if code == 'fulfilled':
        instance_id = response['SpotInstanceRequests'][0]['InstanceId']
        break
    elif code == 'instance-terminated-by-user':
        print('Failure - Instance was terminated by user.\
               Exiting program.  Bye.')
        sys.exit()
    else:
        print('Update - Status received from EC2', code + '...',
              'Trying again...')

ec2.create_tags(
    Resources=[instance_id],
    Tags=[{'Key': DEPLOY_TAG[0], 'Value': DEPLOY_TAG[1]}]
)

print('Success - Spot request fulfilled by EC2 via instance', instance_id)

# deploy app to instances with app_deploy_name (specify ID?)
# via github repo + commit ID (repo and commit should come from the command line)

# put output (logs, models etc.) into S3 bucket

# terminate instance (cancel spot request)
print('Terminating instance...')
response = ec2.terminate_instances(
    InstanceIds=[instance_id]
)

status = response['TerminatingInstances'][0]['CurrentState']['Name']
if status != 'running':
    print('Success - Instance termination command received by EC2.')
else:
    print('Failure - Instance termination failed. Current state is',
          status, '.', 'Use EC2 console terminate instance.')

print('Deploy complete. Bye.')
