#!/bin/bash
set -e

# Create a non-login user for running the application
sudo useradd -r -s /usr/sbin/nologin csye6225 || echo "User already exists"

# Create application directory if it doesn't exist
sudo mkdir -p /opt/myapp

# Set ownership of the application directory
sudo chown -R csye6225:csye6225 /opt/myapp
