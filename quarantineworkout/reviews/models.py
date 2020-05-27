from django.db import models
from django.conf import settings
from stars.models import Star


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    exercise = models.ForeignKey('exercises.exercise',
                                 related_name='reviews',
                                 on_delete=models.CASCADE)
    star = models.ForeignKey(Star, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)