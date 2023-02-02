from dash.stories.models import Story
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class StoryUserModel(models.Model):
    """ Common fields for various user data about specific stories """
    
    story = models.ForeignKey(
        Story, verbose_name=_("Story"), blank=False, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, verbose_name=_("User"), blank=False, null=False, on_delete=models.CASCADE)
    created_on = models.DateTimeField(
        verbose_name=_("Creation date"), auto_now_add=timezone.now, editable=False)

    class Meta:
        abstract = True


class StoryBookmark(StoryUserModel):
    """ An user bookmark flag for a specific story """

    class Meta:
        unique_together = ['story', 'user']


class StoryRating(StoryUserModel):
    """ An user rating for a specific story """

    score = models.PositiveSmallIntegerField(
        verbose_name=_("Score"),
        default=1, blank=False, null=False,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        unique_together = ['story', 'user']
