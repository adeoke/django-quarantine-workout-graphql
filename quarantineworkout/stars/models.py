from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# TODO: CHECK MIN VALUE
class Star(models.Model):
    number = models.IntegerField(validators=[MinValueValidator(0),
                                             MaxValueValidator(5)])
    classification = models.CharField(max_length=25)
