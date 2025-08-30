from django.core.management.base import BaseCommand
from django.utils import timezone
from listings.models import Listing, Booking
from decimal import Decimal
import random
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Seed the database with sample listings and bookings data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--listings',
            type=int,
            default=20,
            help='Number of listings to create (default: 20)'
        )
        parser.add_argument(
            '--bookings',
            type=int,
            default=10,
            help='Number of bookings to create (default: 10)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Listing.objects.all().delete()
            Booking.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared'))

        # Sample data for listings
        sample_listings = [
            {
                'title': 'Cozy Mountain Cabin',
                'description': 'Beautiful wooden cabin with stunning mountain views. Perfect for a peaceful getaway with modern amenities and a fireplace.',
                'price': Decimal('150.00'),
                'available': True
            },
            {
                'title': 'Beachfront Villa',
                'description': 'Luxurious villa steps from the beach. Features private pool, ocean views, and fully equipped kitchen.',
                'price': Decimal('300.00'),
                'available': True
            },
            {
                'title': 'Downtown Luxury Apartment',
                'description': 'Modern apartment in the heart of the city. Walking distance to restaurants, shops, and attractions.',
                'price': Decimal('200.00'),
                'available': True
            },
            {
                'title': 'Rustic Farmhouse',
                'description': 'Charming farmhouse with acres of land. Perfect for families who want to experience country living.',
                'price': Decimal('120.00'),
                'available': True
            },
            {
                'title': 'Ski Resort Condo',
                'description': 'Ski-in/ski-out condo with mountain views. Includes hot tub access and ski storage.',
                'price': Decimal('250.00'),
                'available': True
            },
            {
                'title': 'Desert Oasis',
                'description': 'Unique desert retreat with pool and spa. Stargazing deck and panoramic desert views.',
                'price': Decimal('180.00'),
                'available': True
            },
            {
                'title': 'Historic City Loft',
                'description': 'Renovated loft in a historic building. Exposed brick walls and high ceilings with modern amenities.',
                'price': Decimal('175.00'),
                'available': True
            },
            {
                'title': 'Lakefront Cottage',
                'description': 'Charming cottage on the lake with private dock. Perfect for fishing, swimming, and water activities.',
                'price': Decimal('140.00'),
                'available': True
            },
            {
                'title': 'Tropical Paradise',
                'description': 'Private villa surrounded by tropical gardens. Infinity pool and ocean breezes.',
                'price': Decimal('350.00'),
                'available': True
            },
            {
                'title': 'Alpine Chalet',
                'description': 'Traditional chalet with stunning alpine views. Cozy fireplace and outdoor hot tub.',
                'price': Decimal('220.00'),
                'available': True
            },
            {
                'title': 'Urban Penthouse',
                'description': 'Luxury penthouse with city skyline views. Rooftop terrace and gourmet kitchen.',
                'price': Decimal('400.00'),
                'available': True
            },
            {
                'title': 'Countryside B&B',
                'description': 'Charming bed and breakfast in the countryside. Home-cooked breakfast included.',
                'price': Decimal('95.00'),
                'available': True
            },
            {
                'title': 'Island Retreat',
                'description': 'Private island villa accessible only by boat. Complete privacy and stunning ocean views.',
                'price': Decimal('500.00'),
                'available': True
            },
            {
                'title': 'Wine Country Villa',
                'description': 'Elegant villa in the heart of wine country. Wine tasting tours and vineyard views.',
                'price': Decimal('275.00'),
                'available': True
            },
            {
                'title': 'Modern Treehouse',
                'description': 'Unique treehouse experience with modern comforts. Surrounded by forest and wildlife.',
                'price': Decimal('160.00'),
                'available': True
            },
            {
                'title': 'Coastal Lighthouse',
                'description': 'Converted lighthouse with panoramic ocean views. Historic charm with modern amenities.',
                'price': Decimal('320.00'),
                'available': True
            },
            {
                'title': 'Mountain View Lodge',
                'description': 'Spacious lodge with breathtaking mountain views. Perfect for large groups and families.',
                'price': Decimal('280.00'),
                'available': True
            },
            {
                'title': 'Seaside Bungalow',
                'description': 'Charming bungalow steps from the beach. Private garden and outdoor dining area.',
                'price': Decimal('135.00'),
                'available': True
            },
            {
                'title': 'Artistic Studio Loft',
                'description': 'Creative loft space perfect for artists and designers. High ceilings and natural light.',
                'price': Decimal('155.00'),
                'available': True
            },
            {
                'title': 'Zen Garden Retreat',
                'description': 'Peaceful retreat with Japanese garden and meditation space. Perfect for relaxation.',
                'price': Decimal('190.00'),
                'available': True
            }
        ]

        # Create listings
        listings_created = 0
        for i in range(min(options['listings'], len(sample_listings))):
            listing_data = sample_listings[i]
            # Add some variation to prices
            price_variation = random.uniform(0.8, 1.2)
            listing_data['price'] = round(listing_data['price'] * Decimal(str(price_variation)), 2)
            
            # Randomly set some listings as unavailable
            if random.random() < 0.2:  # 20% chance of being unavailable
                listing_data['available'] = False
            
            listing = Listing.objects.create(**listing_data)
            listings_created += 1
            self.stdout.write(f'Created listing: {listing.title}')

        self.stdout.write(self.style.SUCCESS(f'Successfully created {listings_created} listings'))

        # Create sample bookings
        if options['bookings'] > 0:
            self.create_sample_bookings(options['bookings'])
            self.stdout.write(self.style.SUCCESS(f'Successfully created {options["bookings"]} bookings'))

    def create_sample_bookings(self, num_bookings):
        """Create sample bookings for existing listings"""
        sample_users = [
            'John Smith', 'Emma Johnson', 'Michael Brown', 'Sarah Davis', 'David Wilson',
            'Lisa Anderson', 'Robert Taylor', 'Jennifer Martinez', 'Christopher Garcia',
            'Amanda Rodriguez', 'James Lopez', 'Michelle Gonzalez', 'Daniel Perez',
            'Ashley Torres', 'Matthew Flores', 'Nicole Rivera', 'Joshua Cooper',
            'Stephanie Richardson', 'Andrew Cox', 'Rebecca Howard'
        ]

        available_listings = list(Listing.objects.filter(available=True))
        
        if not available_listings:
            self.stdout.write(self.style.WARNING('No available listings found for bookings'))
            return

        for i in range(num_bookings):
            listing = random.choice(available_listings)
            user = random.choice(sample_users)
            
            # Generate random dates (start date in the future, end date after start date)
            start_date = date.today() + timedelta(days=random.randint(1, 30))
            end_date = start_date + timedelta(days=random.randint(1, 14))
            
            booking = Booking.objects.create(
                listing=listing,
                user=user,
                start_date=start_date,
                end_date=end_date
            )
            
            self.stdout.write(f'Created booking: {booking}') 