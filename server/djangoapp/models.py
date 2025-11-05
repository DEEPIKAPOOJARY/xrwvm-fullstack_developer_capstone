# Uncomment the following imports before adding the Model code

from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


# Create your models here.
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

    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('COUPE', 'Coupe'),
        ('HATCHBACK', 'Hatchback'),
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPES, default='SUV')

    year = models.IntegerField(
        default=datetime.date.today().year,
        validators=[
            MaxValueValidator(datetime.date.today().year),
            MinValueValidator(2015)
        ]
    )

    dealer_id = models.IntegerField()

    #Additional fields
    TRANSMISSION_TYPES = [
        ('AT', 'Automatic'),
        ('MT', 'Manual'),
    ]
    transmission = models.CharField(max_length=2, choices=TRANSMISSION_TYPES, default='AT')

    FUEL_TYPES = [
        ('PETROL', 'Petrol'),
        ('DIESEL', 'Diesel'),
        ('ELECTRIC', 'Electric'),
        ('HYBRID', 'Hybrid'),
    ]
    fuel_type = models.CharField(max_length=10, choices=FUEL_TYPES, default='PETROL')

    color = models.CharField(max_length=50, default="Black")
    mileage = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many
# Car Models, using ForeignKey field)
# - Name
# - Type (CharField with a choices argument to provide limited choices
# such as Sedan, SUV, WAGON, etc.)
# - Year (IntegerField) with min value 2015 and max value 2023
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
