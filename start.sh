#!/bin/bash
#cloud-boothook
echo 'RUNNING USER SCRIPT...'
TIMEZONE=America/Chicago
GIT_REPO=lushdog/DeepLearning
PATH_TO_SCRIPT=DeepLearning/deep_learn_deploy 
SCRIPT_NAME=build_model.py
SCRIPT_OUTPUT_DIR=output
S3_BUCKET=deeplearningoutputs
DL_ENV=tensorflow_p36
# for MXNet(+Keras1) with Python3 (CUDA 9) _____________________ mxnet_p36
# for MXNet(+Keras1) with Python2 (CUDA 9) _____________________ mxnet_p27
# for TensorFlow(+Keras2) with Python3 (CUDA 8) ________________ tensorflow_p36
# for TensorFlow(+Keras2) with Python2 (CUDA 8) ________________ tensorflow_p27
# for Theano(+Keras2) with Python3 (CUDA 9) ____________________ theano_p36
# for Theano(+Keras2) with Python2 (CUDA 9) ____________________ theano_p27
# for PyTorch with Python3 (CUDA 8) ____________________________ pytorch_p36
# for PyTorch with Python2 (CUDA 8) ____________________________ pytorch_p27
# for CNTK(+Keras2) with Python3 (CUDA 8) ______________________ cntk_p36
# for CNTK(+Keras2) with Python2 (CUDA 8) ______________________ cntk_p27
# for Caffe2 with Python2 (CUDA 9) _____________________________ caffe2_p27
# for base Python2 (CUDA 9) ____________________________________ python2
# for base Python3 (CUDA 9) ____________________________________ python3

# Add Python Packages here as needed by build_model.py
# pip install requests

# Filled in by deploy.py
S3_USER_KEY=[key] 
S3_SECRET=[secret]

echo 'INSTALLING PACKAGES...'
# apt-get update
timedatectl set-timezone $TIMEZONE
apt-get install git -y
apt-get install awscli -y

echo 'CLONING REPO...'
cd /home/ubuntu
mkdir deep
cd deep
git clone https://github.com/$GIT_REPO
cd $PATH_TO_SCRIPT
mkdir $SCRIPT_OUTPUT_DIR
chown -R ubuntu .

echo 'RUNNING PYTHON SCRIPT...'
su -c "source /home/ubuntu/anaconda3/bin/activate $DL_ENV && THEANO_FLAGS=device=cuda python $SCRIPT_NAME > $OUTPUT_DIR/$SCRIPT_NAME.log" -s /bin/bash ubuntu

echo 'PACKAGING AND UPLOADING OUTPUT...'
cd $SCRIPT_OUTPUT_DIR
cp /var/log/cloud*.log .
git log --name-status HEAD^..HEAD > git.log
DATE=`date '+%Y-%m-%d-%H.%M.%S'`
OUTPUT_FILE=output.$DATE.tar.gz
tar -zcvf "$OUTPUT_FILE" .
S3_URL=s3://$S3_BUCKET
aws s3 cp $OUTPUT_FILE $S3_URL -O $S3_USER_KEY -W $S3_SECRET

echo 'SHUTTING DOWN INSTANCE...'
# shutdown -P
