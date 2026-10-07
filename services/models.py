from django.db import models
from django.contrib.auth.models import User


class ServiceProvider(models.Model):

    CATEGORY_CHOICES = [
        ('Photography', 'Photography'),
        ('Videography', 'Videography'),

        ('Puncture Shop', 'Puncture Shop'),
        ('Mechanic', 'Mechanic'),
        ('Car Wash', 'Car Wash'),
        ('Bike Service', 'Bike Service'),

        ('Electrician', 'Electrician'),
        ('Plumber', 'Plumber'),
        ('Carpenter', 'Carpenter'),
        ('Painter', 'Painter'),
        ('AC Repair', 'AC Repair'),
        ('Refrigerator Repair', 'Refrigerator Repair'),
        ('Washing Machine Repair', 'Washing Machine Repair'),
        ('Water Purifier Service', 'Water Purifier Service'),
        ('CCTV Installation', 'CCTV Installation'),
        ('Solar Panel Service', 'Solar Panel Service'),
        ('Pest Control', 'Pest Control'),
        ('Cleaning', 'Cleaning'),

        ('Mobile Repair', 'Mobile Repair'),
        ('Laptop Repair', 'Laptop Repair'),
        ('Computer Repair', 'Computer Repair'),

        ('Tailor', 'Tailor'),
        ('Beautician', 'Beautician'),
        ('Makeup Artist', 'Makeup Artist'),
        ('Mehendi Artist', 'Mehendi Artist'),

        ('Tutor', 'Tutor'),
        ('Driving School', 'Driving School'),
        ('Fitness Trainer', 'Fitness Trainer'),
        ('Yoga Trainer', 'Yoga Trainer'),

        ('Cook', 'Cook'),
        ('Laundry', 'Laundry'),
        ('Catering', 'Catering'),

        ('Event Decoration', 'Event Decoration'),
        ('Interior Design', 'Interior Design'),
        ('Taxi Service', 'Taxi Service'),
        ('Packers and Movers', 'Packers and Movers'),

        ('Other', 'Other'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    phone = models.CharField(
        max_length=15
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    location = models.CharField(
        max_length=200
    )

    # Latitude and longitude for nearby-service search
    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    working_hours = models.CharField(
        max_length=100
    )

    image = models.URLField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.first_name