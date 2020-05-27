from django.db import models
from django.conf import settings
from equipment.models import Equipment
from levels.models import Level
from bodyparts.models import BodyPart


# potentially, after loading the users I could create the exercise with a
# review seeds.
class Exercise(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    reps = models.IntegerField(default=10)
    sets = models.IntegerField(default=4)
    description = models.TextField(blank=True)
    body_part = models.ForeignKey(BodyPart, on_delete=models.CASCADE,
                                  null=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                  on_delete=models.CASCADE)
    # problem with one to one is that the equipment can only be used one
    # so that means that you can only have the number of exercises according to
    # the number of equipment types.
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE,
                                  null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    # created_at = models.DateTimeField(auto_now_add=True)
