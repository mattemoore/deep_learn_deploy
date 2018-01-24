#!/bin/bash
apt-get -y update
apt-get -y git
apt-get -y awscli
mkdir /home/deep
cd /home/deep
mkdir /home/deep/output
git fetch [bookmark]
chmod +x ./build_model.py
source activate tensorflow_p36
THEANO_FLAGS=device=cuda python build_model.py 

# Put output (logs, models etc.) into S3 bucket - tag bucket with commit and timstamp

shutdown -P


