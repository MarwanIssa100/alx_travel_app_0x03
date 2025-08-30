#!/bin/bash

# Start Celery Worker Script
echo "Starting Celery Worker..."

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "Error: manage.py not found. Please run this script from the Django project root."
    exit 1
fi

# Check if RabbitMQ is running
if ! pgrep -x "rabbitmq-server" > /dev/null; then
    echo "Warning: RabbitMQ server is not running."
    echo "Please start RabbitMQ first:"
    echo "  sudo systemctl start rabbitmq-server"
    echo ""
fi

# Start Celery worker
echo "Starting Celery worker with info logging..."
celery -A alx_travel_app worker --loglevel=info
