#!/bin/bash
GIT_REPO=lushdog/DeepLearning
PATH_TO_SCRIPT=DeepLearning/deep_learn_deploy 
SCRIPT_NAME=build_model.py
OUTPUT_DIR=output
S3_BUCKET=deep_learning_model_outputs
# TODO: get credentials from deploy.py
# S3_USER_KEY=s3key
# S3_SECRET=s3secret
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
# sudo pip install requests

sudo apt-get update
sudo apt-get install git -y
sudo apt-get install awscli -y
sudo mkdir deep
cd deep
sudo git clone https://github.com/$GIT_REPO
cd $PATH_TO_SCRIPT
sudo mkdir $OUTPUT_DIR
sudo bash -c "source ~/anaconda3/bin/activate $DL_ENV && THEANO_FLAGS=device=cuda python $SCRIPT_NAME > $OUTPUT_DIR/$SCRIPT_NAME.log"
cd $OUTPUT_DIR
# TODO: finish script output push to S3 bucket
# sudo touch git.log
# sudo git log --name-status HEAD^..HEAD >> git.log
# DATE=`date '+%Y-%m-%d-%H.%M.%S'`
# s3=s3://$GIT_REPO-$DATE
# sudo aws s3 mb $s3
# sudo aws s3 cp . $s3  --recursive
sudo shutdown -P