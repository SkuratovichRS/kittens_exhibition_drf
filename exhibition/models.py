from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Breed(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Kitten(models.Model):
    color = models.CharField(max_length=50)
    age = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.CharField(max_length=200)
    breed = models.ForeignKey(Breed, related_name='kittens', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name='kittens', on_delete=models.CASCADE)

    def get_rating(self) -> float:
        ratings = self.ratings.all()
        if not ratings:
            return float(0)
        return round(sum(rating.value for rating in ratings) / len(ratings), 2)


class Rating(models.Model):
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    kitten = models.ForeignKey(Kitten, related_name='ratings', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'kitten')
