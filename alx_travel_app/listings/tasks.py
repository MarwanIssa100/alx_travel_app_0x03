from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@shared_task
def send_booking_confirmation_email(booking_id):
    """
    Send a booking confirmation email to the user.
    This is a shared task that can be called from anywhere in the application.
    """
    from .models import Booking
    
    try:
        # Get the booking object
        booking = Booking.objects.get(id=booking_id)
        
        # Prepare email content
        subject = f'Booking Confirmation - {booking.listing.title}'
        
        # Create HTML content
        html_message = f"""
        <html>
        <body>
            <h2>Booking Confirmation</h2>
            <p>Dear {booking.user},</p>
            <p>Your booking has been confirmed successfully!</p>
            
            <h3>Booking Details:</h3>
            <ul>
                <li><strong>Property:</strong> {booking.listing.title}</li>
                <li><strong>Check-in:</strong> {booking.start_date}</li>
                <li><strong>Check-out:</strong> {booking.end_date}</li>
                <li><strong>Price:</strong> ${booking.listing.price}</li>
            </ul>
            
            <p>Thank you for choosing our service!</p>
            <p>Best regards,<br>ALX Travel App Team</p>
        </body>
        </html>
        """
        
        # Create plain text content
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[f'{booking.user}@example.com'],  # In a real app, you'd use actual user email
            html_message=html_message,
            fail_silently=False,
        )
        
        print(f"Booking confirmation email sent successfully for booking {booking_id}")
        return True
        
    except Booking.DoesNotExist:
        print(f"Booking with id {booking_id} does not exist")
        return False
    except Exception as e:
        print(f"Error sending booking confirmation email: {str(e)}")
        return False


@shared_task
def send_payment_confirmation_email(payment_id):
    """
    Send a payment confirmation email to the user.
    """
    from .models import Payment
    
    try:
        # Get the payment object
        payment = Payment.objects.get(id=payment_id)
        booking = payment.booking
        
        # Prepare email content
        subject = f'Payment Confirmation - {booking.listing.title}'
        
        # Create HTML content
        html_message = f"""
        <html>
        <body>
            <h2>Payment Confirmation</h2>
            <p>Dear {booking.user},</p>
            <p>Your payment has been processed successfully!</p>
            
            <h3>Payment Details:</h3>
            <ul>
                <li><strong>Transaction ID:</strong> {payment.transaction_id}</li>
                <li><strong>Amount:</strong> ${payment.amount}</li>
                <li><strong>Status:</strong> {payment.status}</li>
                <li><strong>Date:</strong> {payment.payment_date}</li>
            </ul>
            
            <h3>Booking Details:</h3>
            <ul>
                <li><strong>Property:</strong> {booking.listing.title}</li>
                <li><strong>Check-in:</strong> {booking.start_date}</li>
                <li><strong>Check-out:</strong> {booking.end_date}</li>
            </ul>
            
            <p>Thank you for your payment!</p>
            <p>Best regards,<br>ALX Travel App Team</p>
        </body>
        </html>
        """
        
        # Create plain text content
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[f'{booking.user}@example.com'],  # In a real app, you'd use actual user email
            html_message=html_message,
            fail_silently=False,
        )
        
        print(f"Payment confirmation email sent successfully for payment {payment_id}")
        return True
        
    except Payment.DoesNotExist:
        print(f"Payment with id {payment_id} does not exist")
        return False
    except Exception as e:
        print(f"Error sending payment confirmation email: {str(e)}")
        return False
