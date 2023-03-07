from dash.stories.models import Story
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class StorySettings(models.Model):
    """ Various settings per Story """
    
    story = models.OneToOneField(
        Story,
        verbose_name=_("Story"), on_delete=models.CASCADE)
    reward_points = models.PositiveSmallIntegerField(
        verbose_name=_("Reward points"),
        default=0, blank=False, null=False,
        help_text=_("How many points does an user earn for reading this story"))
    display_rating = models.BooleanField(
        verbose_name=_("Display the user rating"), default=True,
        help_text=_("Display or hide the user rating for this story"))
    cached_rating = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, editable=False)

    class Meta:
        verbose_name = _("Story settings")
        verbose_name_plural = _("Story settings")


class StoryUserModel(models.Model):
    """ Common fields for keeping user data about specific stories """
    
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
        verbose_name = _("Story bookmark")
        verbose_name_plural = _("Story bookmarks")
        unique_together = ['story', 'user']


class StoryRating(StoryUserModel):
    """ An user rating for a specific story """

    score = models.PositiveSmallIntegerField(
        verbose_name=_("Score"),
        default=1, blank=False, null=False,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        verbose_name = _("Story rating")
        verbose_name_plural = _("Story ratings")
        unique_together = ['story', 'user']


class StoryRead(StoryUserModel):
    """ Save the date when the user first read a story """

    class Meta:
        verbose_name = _("Story read")
        verbose_name_plural = _("Story reads")
        unique_together = ['story', 'user']


class StoryReward(StoryUserModel):
    """ Reward points received by an user for reading a story """

    points = models.PositiveSmallIntegerField(
        verbose_name=_("Points"),
        default=0, blank=False, null=False
    )

    class Meta:
        verbose_name = _("Story reward")
        verbose_name_plural = _("Story rewards")
        unique_together = ['story', 'user']


@receiver(models.signals.post_save, sender=StoryRating)
def calculate_story_rating(sender, **kwargs):
    # TODO
    print("Someone rated a story...")
