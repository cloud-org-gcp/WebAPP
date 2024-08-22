#!/bin/bash
set -e

# Install the Google Cloud Ops Agent
echo "Installing Google Cloud Ops Agent..."
curl -sSO https://dl.google.com/cloudagents/add-google-cloud-ops-agent-repo.sh
sudo bash add-google-cloud-ops-agent-repo.sh --also-install

sudo mkdir -p /var/log/myapp
sudo chown -R csye6225:csye6225 /var/log/myapp

# Configure the Ops Agent for application logs
echo "Configuring Ops Agent for logging..."
sudo mkdir -p /etc/google-cloud-ops-agent/config.yaml.d
sudo tee /etc/google-cloud-ops-agent/config.yaml > /dev/null <<EOF
logging:
  receivers:
    fastapi_log:
      type: files
      include_paths:
        - /var/log/myapp/*.log
  service:
    pipelines:
      fastapi_pipeline:
        receivers: [fastapi_log]
EOF

# Restart the Ops Agent to apply the configuration
echo "Restarting Ops Agent to apply configuration..."

sudo systemctl daemon-reload
sudo systemctl enable google-cloud-ops-agent
sudo systemctl restart google-cloud-ops-agent

echo "Google Cloud Ops Agent installation and configuration completed."
