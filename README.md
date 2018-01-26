## What does this do?

 - Test models on your desktop then quickly and easily build full models on DL instances on AWS
- Run *deploy.py* and walk away, knowing you won't spend any more money than necessary to build your models.
- This script automatically requests a Deep Learning GPU spot instance, runs a script from source control, archives the output and terminates the instance.
- Save time and money. AWS deep learning spot instances are 30% cheaper than on-demand instances.

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
- After start.sh completes, the instance is shutdown (terminated as it is a spot request)
- Output (e.g. .pkl files and logs) available in S3 directory

## Notes/Ideas
- Datasets need to be downloaded via the python script specified in start.sh Downloading massive datasets for every run could incur significant data transfer costs.
- 