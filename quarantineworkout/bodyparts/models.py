"""bodypart models module"""

from django.db import models


class BodyPart(models.Model):
    """bodyparts ORM table mappings class"""
    name = models.CharField(max_length=30)
