## What does this do?
 
- Test models on your desktop then 'fire and forget' building full models on Deep Learning Amazon AWS spot instances
- Instances are created, used and terminated automatically
- Python script output (model weights and logs) available in S3 bucket after instance termination
- More lightweight than using Ansible, Chef or Terraform
- Save money. AWS deep learning spot instances are 30% cheaper than on-demand instances.

## Requirements
- Python 3.6
- Boto3
- awscli

## Setup
- Run awscli to set AWS keys (need EC2 and S3 permissions) and region
- Put contents of this repo into root of code to deploy to AWS instance
- Modify parameters in *start.sh* (mandatory)
- Modify parameters in *deploy.py* (not mandatory)

## Usage and Flow
- Run 'deploy.py' to create spot instance request 
- When request is fulfilled a Deep Learning instance is created that runs *start.sh* on the instance at bootup
- *start.sh* will pull down your script from GitHub and run it 
- After script completes, *start.sh* will terminate instance
- Script output (e.g. models, weights and logs) folder zipped and pushed to S3 bucket

## Notes/Ideas
- Datasets need to be downloaded via the python script specified in start.sh.  Downloading massive datasets for every run could incur significant data transfer costs.  Support for attaching a persistent volume?