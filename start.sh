#!/bin/bash
#cloud-boothook
echo 'RUNNING USER SCRIPT...'
GIT_REPO=lushdog/DeepLearning
PATH_TO_SCRIPT=DeepLearning/deep_learn_deploy 
SCRIPT_NAME=build_model.py
OUTPUT_DIR=output
S3_BUCKET=deep_learning_outputs
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
# e.g. sudo pip install requests

#automatically filled in by deploy.py
S3_USER_KEY=[key] 
S3_SECRET=[secret]

echo 'UPDATING PACKAGES...'
apt-get update
apt-get install git -y
apt-get install awscli -y

echo 'CLONING REPO...'
cd /home/ubuntu
mkdir deep
cd deep
git clone https://github.com/$GIT_REPO
cd $PATH_TO_SCRIPT
mkdir $OUTPUT_DIR
chown -R ubuntu .

echo 'RUNNING PYTHON DL SCRIPT...'
# sudo bash -c "source /home/ubuntu/anaconda3/bin/activate $DL_ENV && THEANO_FLAGS=device=cuda python $SCRIPT_NAME > $OUTPUT_DIR/$SCRIPT_NAME.log" -s /bin/sh ubuntu
su -c "source /home/ubuntu/anaconda3/bin/activate $DL_ENV && THEANO_FLAGS=device=cuda python $SCRIPT_NAME > $OUTPUT_DIR/$SCRIPT_NAME.log" -s /bin/bash ubuntu
cd $OUTPUT_DIR

echo 'PACKAGING AND UPLOADING OUTPUT...'
# TODO: finish script output push to S3 bucket
# sudo cp /var/log/cloud-init-output.log .
# sudo touch git.log
# sudo git log --name-status HEAD^..HEAD >> git.log
# DATE=`date '+%Y-%m-%d-%H.%M.%S'`
# s3=s3://$GIT_REPO-$DATE
# sudo aws s3 mb $s3
# sudo aws s3 cp . $s3  --recursive

echo 'SHUTTING DOWN INSTANCE...'
# sudo shutdown -P
