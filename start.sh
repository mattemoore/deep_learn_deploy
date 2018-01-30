
#!/bin/bash
$GIT_REPO=https://github.com/lushdog/DeepLearning
$PATH_TO_SCRIPT=DeepLearning/deep_learn_deploy 
$SCRIPT_NAME=build_model.py
$OUTPUT_DIR=output
# for MXNet(+Keras1) with Python3 (CUDA 9) _____________________ source activate mxnet_p36
# for MXNet(+Keras1) with Python2 (CUDA 9) _____________________ source activate mxnet_p27
# for TensorFlow(+Keras2) with Python3 (CUDA 8) ________________ source activate tensorflow_p36
# for TensorFlow(+Keras2) with Python2 (CUDA 8) ________________ source activate tensorflow_p27
# for Theano(+Keras2) with Python3 (CUDA 9) ____________________ source activate theano_p36
# for Theano(+Keras2) with Python2 (CUDA 9) ____________________ source activate theano_p27
# for PyTorch with Python3 (CUDA 8) ____________________________ source activate pytorch_p36
# for PyTorch with Python2 (CUDA 8) ____________________________ source activate pytorch_p27
# for CNTK(+Keras2) with Python3 (CUDA 8) ______________________ source activate cntk_p36
# for CNTK(+Keras2) with Python2 (CUDA 8) ______________________ source activate cntk_p27
# for Caffe2 with Python2 (CUDA 9) _____________________________ source activate caffe2_p27
# for base Python2 (CUDA 9) ____________________________________ source activate python2
# for base Python3 (CUDA 9) ____________________________________ source activate python3
source activate tensorflow_p36

# Add more Python Packages here as needed by build_model.py
sudo pip install requests

sudo apt-get update
sudo apt-get install git -y
sudo apt-get install awscli -y
sudo mkdir deep
cd deep
sudo git clone $GIT_REPO
# chmod -R +x -name '*.py'
cd $PATH_TO_SCRIPT
sudo mkdir $OUTPUT_DIR
dt=$(date '+%d/%m/%Y %H:%M:%S')
THEANO_FLAGS=device=cuda python $SCRIPT_NAME > '$OUTPUT_DIR\$dt.log'
cd $OUTPUT_DIR
# TODO: Put output (logs, models etc.) into S3 bucket - tag bucket with commit and timstamp
sudo shutdown -P

