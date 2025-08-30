#!/usr/bin/env python3
"""
Simple test script to verify Celery setup
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')

# Setup Django
django.setup()

def test_celery_import():
    """Test if Celery can be imported and configured"""
    try:
        from alx_travel_app.celery import app
        print("✓ Celery app imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import Celery app: {e}")
        return False

def test_task_import():
    """Test if tasks can be imported"""
    try:
        from listings.tasks import send_booking_confirmation_email, send_payment_confirmation_email
        print("✓ Email tasks imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import tasks: {e}")
        return False

def test_settings():
    """Test if Celery settings are configured"""
    try:
        from django.conf import settings
        print(f"✓ Celery broker URL: {settings.CELERY_BROKER_URL}")
        print(f"✓ Email backend: {settings.EMAIL_BACKEND}")
        print(f"✓ Email host: {settings.EMAIL_HOST}")
        return True
    except Exception as e:
        print(f"✗ Failed to check settings: {e}")
        return False

def main():
    print("Testing Celery Setup...")
    print("=" * 40)
    
    tests = [
        test_celery_import,
        test_task_import,
        test_settings,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! Celery setup looks good.")
    else:
        print("✗ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()
