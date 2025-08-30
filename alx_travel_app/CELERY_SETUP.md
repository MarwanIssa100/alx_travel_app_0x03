# Celery Setup Guide

This guide explains how to set up and test Celery with RabbitMQ for background email tasks in the ALX Travel App.

## Prerequisites

1. **RabbitMQ Server**: Make sure RabbitMQ is installed and running
2. **Python Dependencies**: All required packages are already in `requirement.txt`

## Installation Steps

### 1. Install RabbitMQ (if not already installed)

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install rabbitmq-server
sudo systemctl start rabbitmq-server
sudo systemctl enable rabbitmq-server
```

**macOS:**
```bash
brew install rabbitmq
brew services start rabbitmq
```

### 2. Install Python Dependencies

```bash
pip install -r alx_travel_app/requirement.txt
```

### 3. Configure Email Settings

Add your email credentials to your `.env` file:

```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**Note**: For Gmail, you'll need to use an App Password instead of your regular password.

## Running Celery

### 1. Start RabbitMQ (if not already running)

```bash
sudo systemctl start rabbitmq-server
```

### 2. Start Celery Worker

In the project root directory (`alx_travel_app`), run:

```bash
celery -A alx_travel_app worker --loglevel=info
```

### 3. Start Celery Beat (Optional - for scheduled tasks)

```bash
celery -A alx_travel_app beat --loglevel=info
```

### 4. Start Django Development Server

```bash
python manage.py runserver
```

## Testing the Setup

### 1. Test Celery Connection

```bash
python manage.py test_celery
```

### 2. Test Email Functionality

```bash
python manage.py test_celery --create-test-booking
```

### 3. Test via API

1. Start the Django server
2. Create a booking via the API endpoint
3. Check the Celery worker logs for email task execution

## API Endpoints

- **Create Booking**: `POST /api/bookings/`
- **Create Payment**: `POST /api/payments/`

Both endpoints will automatically trigger email confirmation tasks.

## Email Tasks

### Booking Confirmation Email
- **Task**: `send_booking_confirmation_email`
- **Triggered**: When a new booking is created
- **Content**: Booking details, property information, dates

### Payment Confirmation Email
- **Task**: `send_payment_confirmation_email`
- **Triggered**: When a payment is processed
- **Content**: Payment details, transaction ID, booking information

## Troubleshooting

### 1. RabbitMQ Connection Issues

Check if RabbitMQ is running:
```bash
sudo systemctl status rabbitmq-server
```

### 2. Celery Worker Issues

Make sure you're in the correct directory:
```bash
cd alx_travel_app
celery -A alx_travel_app worker --loglevel=info
```

### 3. Email Issues

- Verify email credentials in `.env` file
- For Gmail, ensure you're using an App Password
- Check if your email provider allows SMTP access

### 4. Task Not Executing

- Ensure Celery worker is running
- Check Celery worker logs for errors
- Verify task is properly registered

## Monitoring

### Celery Flower (Optional)

Install and run Celery Flower for web-based monitoring:

```bash
pip install flower
celery -A alx_travel_app flower
```

Access the web interface at: `http://localhost:5555`

## Production Considerations

1. **Use Redis**: Consider using Redis instead of RPC for result backend
2. **Supervisor**: Use supervisor to manage Celery processes
3. **Logging**: Configure proper logging for production
4. **Email Service**: Use a dedicated email service (SendGrid, Mailgun, etc.)
5. **Security**: Secure RabbitMQ with proper authentication

## Files Modified/Created

- `alx_travel_app/settings.py` - Added Celery and email configurations
- `alx_travel_app/celery.py` - Created Celery app configuration
- `alx_travel_app/__init__.py` - Added Celery app import
- `listings/tasks.py` - Created email tasks
- `listings/views.py` - Modified to trigger email tasks
- `listings/management/commands/test_celery.py` - Created testing command
