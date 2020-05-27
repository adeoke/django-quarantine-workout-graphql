from django.db import models


class Level(models.Model):
    difficulty = models.CharField(max_length=30)
