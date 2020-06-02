"""Equipment models module"""
from django.db import models


class Equipment(models.Model):
    """Equipment ORM class"""
    name = models.CharField(max_length=50)
