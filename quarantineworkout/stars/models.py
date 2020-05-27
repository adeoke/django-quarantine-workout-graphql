from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# TODO: to test minimum validation.
class Star(models.Model):
    number = models.IntegerField(validators=[MinValueValidator(1),
                                             MaxValueValidator(5)])
    classification = models.CharField(max_length=25)
