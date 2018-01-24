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


AWS_REGION = 'us-east-1'
DEEP_LEARN_AMI = 'Deep Learning AMI (Ubuntu) Version 2.0'
DEEP_LEARN_INSTANCE_TYPE = 'p2.xlarge'
DEPLOY_TAG = ['Name', 'DeepLearningBox']

print('Hello. Starting deploy...')

# Connect to EC2
ec2 = boto3.client('ec2')

# Requst deep learning Spot Instance
print('Retrieving deep learning', '"' + DEEP_LEARN_AMI + '"',
      'AMI id for region', AWS_REGION + '...')
image_filter = [{'Name': 'name',
                 'Values': [DEEP_LEARN_AMI]}]
images = ec2.describe_images(Filters=image_filter)
image_id = images['Images'][0]['ImageId']
print('Success - Retrieved AMI ', image_id)

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
    # TODO: check timeout and cancel if past timeout
    # if time_elapsed > timeout:
        # print('Spot Request timeout reached.  Last status was', code)
        # print('Cancelling Spot Request...')
        # print('Exiting program.  Bye.')
        break

ec2.create_tags(
    Resources=[instance_id],
    Tags=[{'Key': DEPLOY_TAG[0], 'Value': DEPLOY_TAG[1]}]
)

print('Success - Spot request fulfilled by EC2 via instance', instance_id)
print('Deploy complete.')
