from django.core.management.base import BaseCommand
from django.utils import timezone
from listings.models import Listing, Booking
from listings.tasks import send_booking_confirmation_email


class Command(BaseCommand):
    help = 'Test Celery email functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-test-booking',
            action='store_true',
            help='Create a test booking and trigger email',
        )

    def handle(self, *args, **options):
        if options['create_test_booking']:
            self.create_test_booking_and_email()
        else:
            self.test_celery_connection()

    def test_celery_connection(self):
        """Test if Celery is properly configured"""
        self.stdout.write(
            self.style.SUCCESS('Testing Celery connection...')
        )
        
        try:
            # Import Celery app
            from alx_travel_app.celery import app
            
            # Test basic Celery functionality
            result = app.control.inspect().active()
            self.stdout.write(
                self.style.SUCCESS('✓ Celery is running and accessible')
            )
            
            # Test task registration
            registered_tasks = app.tasks.keys()
            if 'listings.tasks.send_booking_confirmation_email' in registered_tasks:
                self.stdout.write(
                    self.style.SUCCESS('✓ Email task is registered')
                )
            else:
                self.stdout.write(
                    self.style.WARNING('⚠ Email task not found in registered tasks')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Celery connection failed: {str(e)}')
            )

    def create_test_booking_and_email(self):
        """Create a test booking and trigger email"""
        self.stdout.write(
            self.style.SUCCESS('Creating test booking and triggering email...')
        )
        
        try:
            # Get or create a test listing
            listing, created = Listing.objects.get_or_create(
                title='Test Property',
                defaults={
                    'description': 'A beautiful test property for testing',
                    'price': 150.00,
                    'available': True
                }
            )
            
            if created:
                self.stdout.write('✓ Created test listing')
            else:
                self.stdout.write('✓ Using existing test listing')
            
            # Create a test booking
            booking = Booking.objects.create(
                listing=listing,
                user='testuser',
                start_date=timezone.now().date(),
                end_date=(timezone.now() + timezone.timedelta(days=3)).date()
            )
            
            self.stdout.write(f'✓ Created test booking with ID: {booking.id}')
            
            # Trigger the email task
            task_result = send_booking_confirmation_email.delay(booking.id)
            self.stdout.write(f'✓ Email task triggered with task ID: {task_result.id}')
            
            # Wait a moment for the task to complete
            import time
            time.sleep(2)
            
            # Check task status
            if task_result.ready():
                if task_result.successful():
                    self.stdout.write(
                        self.style.SUCCESS('✓ Email task completed successfully')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'✗ Email task failed: {task_result.result}')
                    )
            else:
                self.stdout.write(
                    self.style.WARNING('⚠ Email task is still running...')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Error creating test booking: {str(e)}')
            )
