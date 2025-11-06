from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    country = models.CharField(max_length=100, default="Unknown")
    founded_year = models.IntegerField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    logo_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.country})"


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    # Car type options
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('COUPE', 'Coupe'),
        ('HATCHBACK', 'Hatchback'),
    ]
    type = models.CharField(
        max_length=10,
        choices=CAR_TYPES,
        default='SUV'
    )

    year = models.IntegerField(
        default=datetime.date.today().year,
        validators=[
            MaxValueValidator(datetime.date.today().year),
            MinValueValidator(2015)
        ]
    )

    dealer_id = models.IntegerField()

    # Transmission options
    TRANSMISSION_TYPES = [
        ('AT', 'Automatic'),
        ('MT', 'Manual'),
    ]
    transmission = models.CharField(
        max_length=2,
        choices=TRANSMISSION_TYPES,
        default='AT'
    )

    # Fuel type options
    FUEL_TYPES = [
        ('PETROL', 'Petrol'),
        ('DIESEL', 'Diesel'),
        ('ELECTRIC', 'Electric'),
        ('HYBRID', 'Hybrid'),
    ]
    fuel_type = models.CharField(
        max_length=10,
        choices=FUEL_TYPES,
        default='PETROL'
    )

    color = models.CharField(max_length=50, default="Black")
    mileage = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"
