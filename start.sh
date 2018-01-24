
#!/bin/bash
$GIT_REPO=https://github.com/lushdog/DeepLearning
$PATH_TO_SCRIPT=DeepLearning/deep_learn_deploy 
$SCRIPT_NAME=build_model.py
$OUTPUT_DIR=output

sudo apt-get update
sudo apt-get install git -y
sudo apt-get install awscli -y
source activate tensorflow_p36
sudo mkdir deep
cd deep
sudo git clone $GIT_REPO
# chmod -R +x -name '*.py'
cd $PATH_TO_SCRIPT
sudo mkdir $OUTPUT_DIR
THEANO_FLAGS=device=cuda python $SCRIPT_NAME
cd $OUTPUT_DIR
# TODO: Put output (logs, models etc.) into S3 bucket - tag bucket with commit and timstamp
sudo shutdown -P

