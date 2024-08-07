#!/bin/bash

# Create a systemd service file for the FastAPI application
sudo tee /etc/systemd/system/myapp.service > /dev/null <<EOF
[Unit]
Description=My FastAPI Application

[Service]
WorkingDirectory=/opt/myapp/code_files
ExecStart=/usr/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
User=csye6225
Group=csye6225
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd, enable, and start the service
sudo systemctl daemon-reload
sudo systemctl enable myapp.service
sudo systemctl start myapp.service
