from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Listing , Booking ,Payment
from .serializers import ListingSerializer, BookingSerializer, PaymentSerializer
import requests
import json

# Create your views here.

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            # Get booking data from request
            booking_id = request.data.get('booking')
            amount = request.data.get('amount')
            
            if not booking_id or not amount:
                return Response(
                    {'error': 'Booking ID and amount are required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get the booking
            try:
                booking = Booking.objects.get(id=booking_id)
            except Booking.DoesNotExist:
                return Response(
                    {'error': 'Booking not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Prepare payload for Chapa API
            payload = {
                "amount": str(amount),
                "currency": "ETB",
                "email": f"{booking.user}@example.com",  # Using booking user as email
                "phone_number": "1234567890",  # Default phone number
                "customization": {
                    "title": f"Payment for {booking.listing.title}",
                    "description": f"Booking from {booking.start_date} to {booking.end_date}"
                }
            }
            
            headers = {
                'Authorization': 'Bearer CHASECK-xxxxxxxxxxxxxxxx',
                'Content-Type': 'application/json'
            }
            
            # Make API call to Chapa
            response = requests.post(
                "https://api.chapa.co/v1/transaction/initialize", 
                json=payload, 
                headers=headers
            )
            
            if response.status_code == 200:
                response_data = response.json()
                transaction_id = response_data.get('data', {}).get('reference', '')
                
                # Create Payment record
                payment_data = {
                    'transaction_id': transaction_id,
                    'booking': booking_id,
                    'amount': amount,
                    'status': 'Pending'
                }
                
                serializer = self.get_serializer(data=payment_data)
                if serializer.is_valid():
                    payment = serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {'error': 'Payment gateway error', 'details': response.text}, 
                    status=status.HTTP_502_BAD_GATEWAY
                )
                
        except Exception as e:
            return Response(
                {'error': 'Internal server error', 'details': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )