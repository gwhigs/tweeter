from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from model_utils.models import TimeStampedModel


@python_2_unicode_compatible
class Tweet(TimeStampedModel):
    text = models.CharField(max_length=140)
    tweeted = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
