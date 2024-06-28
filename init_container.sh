#!/bin/bash
set -e
echo "Starting ssh......................"
service ssh start
echo 'Starting uvicorn'
exec uvicorn main:app --reload --host 0.0.0.0 --port 8910
#Local: 8910. Azure:80