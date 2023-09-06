#!/bin/bash

# Source the configuration file
source instance_config.sh

# Commands to run on the remote Oracle Compute instance
REMOTE_COMMANDS="
sudo yum install httpd -y
sudo systemctl start httpd
sudo systemctl enable httpd
sudo firewall-cmd --permanent --zone=public --add-service=http
sudo firewall-cmd --reload
"

# Connect to the remote instance and execute commands
ssh -i "$SSH_KEY" $REMOTE_USER@$REMOTE_HOST "$REMOTE_COMMANDS"
