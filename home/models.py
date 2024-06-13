from django.db import models
from rest_framework import serializers


class Color(models.Model):
    color_name = models.CharField(max_length=100)

    def __str__(self):
        return self.color_name


# Create your models here.
class Person(models.Model):
    color = models.ForeignKey(
        Color, on_delete=models.CASCADE, null=True, blank=True, related_name="color"
    )
    name = models.CharField(max_length=100)
    age = models.IntegerField()
