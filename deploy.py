import base64
import sys
from time import sleep
import boto3

# What does this do?
# Test models on your desktop then when you are ready to build the full model, commit script to github and then use 
# this tool to build the full models using AWS GPU compute instances. 
# Save time and money - AWS deep learning spot instances are 30% cheaper than on-demand instances.
# Run 'deploy.py' and walk away, knowing you won't spend any more money than necessary to build your models.
# This script automatically requests a Deep Learning spot instance, runs a script from source control, archives the output and terminates the instance.

# Requirements:
# Python 3.6
# Boto3
# awscli

# Setup:
# Run awscli to set keys (need EC2 and S3 permissions) and region
# Put contents of this repo into root of code to deploy
# Modify code structure and github settings in 'start.sh' (mandatory)
# Modify AWS instance settings in 'deploy.py' (not mandatory)

# Usage and Flow:
# Run 'deploy.py' to create spot instance request
# When request is fulfilled a Deep Learning instance is created that runs 'start.sh' at bootup
# After start.sh completes, the instance is shutdown (terminated as it is a spot request)
# Output (e.g. .pkl files and logs) available in S3 directory

DEEP_LEARN_AMI = 'Deep Learning AMI (Ubuntu) Version 2.0'
DEEP_LEARN_INSTANCE_TYPE = 'p2.xlarge'
DEPLOY_TAG = ['Name', 'DeepLearningBox']

print('Hello. Starting deploy...')

# Connect to EC2
ec2 = boto3.client('ec2')

# Requst deep learning Spot Instance
print('Retrieving deep learning', '"' + DEEP_LEARN_AMI + '"',
      'AMI id for region', ec2._client_config.region_name + '...')
image_filter = [{'Name': 'name',
                 'Values': [DEEP_LEARN_AMI]}]
images = ec2.describe_images(Filters=image_filter)
image_id = images['Images'][0]['ImageId']
print('Success - Retrieved AMI', image_id)

print('Requesting deep learning spot instance from EC2...')

with open('start.sh', 'r') as file:
    user_data = file.read()
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
      'created by EC2.\nWaiting for fulfillment from EC2...')


# Wait for Spot Instance Request fulfillment
request_filter = [{'Name': 'spot-instance-request-id', 'Values': [request_id]}]
while True:
    sleep(10)
    response = ec2.describe_spot_instance_requests(Filters=request_filter)

    if len(response['SpotInstanceRequests']) > 0:
        code = response['SpotInstanceRequests'][0]['Status']['Code']
        if code == 'fulfilled':
            instance_id = response['SpotInstanceRequests'][0]['InstanceId']
            break
        elif code == 'instance-terminated-by-user':
            print('Failure - Instance was terminated by user.\
                   Exiting program.  Bye.')
            sys.exit()
        else:
            print('Update - Spot requst not fulfilled yet.\
                   Current status', code + '...',
                  'Querying again...')
    else:
        print('Update - Spot instance details not available yet.',
              'Querying again...')

ec2.create_tags(
    Resources=[instance_id],
    Tags=[{'Key': DEPLOY_TAG[0], 'Value': DEPLOY_TAG[1]}]
)

print('Success - Spot request fulfilled by EC2 via instance', instance_id)
print('Deploy complete.')
