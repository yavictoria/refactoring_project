"""Database models for food tracking."""

from django.db import models
from django.contrib.auth.models import User

class Food(models.Model):
    """Model representing a food item with nutritional values."""

    name = models.CharField(max_length=100)
    carbs = models.FloatField()
    protein = models.FloatField()
    fats = models.FloatField()
    calories = models.IntegerField()

    def __str__(self):
        return str(self.name)

class Consume(models.Model):
    """Model representing a user's consumed food record."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_consumed = models.ForeignKey(Food, on_delete=models.CASCADE)
