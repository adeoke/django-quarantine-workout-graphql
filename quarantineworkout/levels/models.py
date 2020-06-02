"""Levels model module"""
from django.db import models


class Level(models.Model):
    """Level table mappings"""
    difficulty = models.CharField(max_length=30)
