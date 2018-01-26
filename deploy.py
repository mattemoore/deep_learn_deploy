import base64
import sys
from time import sleep
import boto3

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
