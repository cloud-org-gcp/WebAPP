#!/bin/bash
set -e

# Update the system
sudo yum update -y

# Install necessary packages
sudo yum install -y python3 python3-pip unzip

# Unzip the archive to /tmp
sudo unzip /tmp/app.zip -d /tmp

# Move the contents from /tmp to /opt/myapp
sudo mv /tmp/code_files /opt/myapp/
sudo mv /tmp/requirements.txt /opt/myapp/

# Navigate to the target directory and install dependencies
cd /opt/myapp
sudo python3 -m venv venv

# Change ownership of the virtual environment to the current user to avoid permission issues
sudo chown -R $(whoami):$(whoami) /opt/myapp/venv

source venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt