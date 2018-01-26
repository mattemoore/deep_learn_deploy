## What does this do?
 
- Test models on your desktop then build full models on DL spot instances on AWS
- Instances are created, used and terminated automatically
- More lightweight than using Ansible, Chef or Terraform
- Save money. AWS deep learning spot instances are 30% cheaper than on-demand instances.

## Requirements
- Python 3.6
- Boto3
- awscli

## Setup
- Run awscli to set AWS keys (need EC2 and S3 permissions) and region
- Put contents of this repo into root of code to deploy on AWS instance
- Modify code structure and github settings in *start.sh* (mandatory)
- Modify AWS instance settings in *deploy.py* (not mandatory)

## Usage and Flow
- Run 'deploy.py' to create spot instance request 
- When request is fulfilled a Deep Learning instance is created that runs *start.sh* at bootup
- *start.sh* will pull down your DL script from GitHub and run it 
- After DL script completes start.sh will terminate instance
- DL script output (e.g. .pkl files and logs) available in S3 directory

## Notes/Ideas
- Datasets need to be downloaded via the python script specified in start.sh Downloading massive datasets for every run could incur significant data transfer costs.
- Support for attaching a persistent volume?