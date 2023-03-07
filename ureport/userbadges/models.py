from functools import partial

from dash.categories.models import Category
from dash.orgs.models import Org
from dash.utils import generate_file_path
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ureport.storyextras.models import StoryRead


ITEM_TYPE_CHOICES = (
    ("S", _("Stories")),
    ("P", _("Polls")),
)


class VisibleManager(models.Manager):
    """ Filter to return only visible items """

    def get_queryset(self):
        return super().get_queryset().filter(is_visible=True)


class AcceptedManager(models.Manager):
    """ Filter to return only items which have an accepted_on date """

    def get_queryset(self):
        return super().get_queryset().filter(accepted_on__isnull=False)


class BadgeType(models.Model):
    org = models.ForeignKey(
        Org, verbose_name=_("Organisation"),
        blank=False, null=False, on_delete=models.CASCADE)
    title = models.CharField(
        verbose_name=_("Title"),max_length=50, blank=False, null=False)
    image = models.ImageField(
        verbose_name=_("Image"), 
        upload_to=partial(generate_file_path, "userbadges"), 
        help_text=_("The badge icon file"))
    description = models.CharField(
        verbose_name=_("Short description"),
        max_length=250, blank=True, null=False, default="")
    is_visible = models.BooleanField(
        verbose_name=_("Display this item"),
        default=True, db_index=True)
    item_type = models.CharField(
        _("Validation item type"),
        max_length=1, choices=ITEM_TYPE_CHOICES, default="S",
        help_text=_("Badge validation applies to Stories or Polls"))
    item_category = models.ForeignKey(
        Category, verbose_name=_("Validation item category"),
        blank=True, null=True, on_delete=models.PROTECT,
        help_text=_("Restrict badge validation to a specific category"))
    item_count = models.PositiveSmallIntegerField(
        verbose_name=_("Validation item count"),
        default=10000, blank=False, null=False,
        validators=[MinValueValidator(1), MaxValueValidator(10000)],
        help_text=_("Offer this badge to users who completed this number of items"))

    objects = models.Manager()
    visible = VisibleManager()

    class Meta:
        verbose_name = _("Badge type")
        verbose_name_plural = _("Badge types")
        unique_together = ("org", "title")


class UserBadge(models.Model):
    badge_type = models.ForeignKey(
        BadgeType, verbose_name=_("Badge type"), 
        blank=False, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, verbose_name=_("User"), 
        blank=False, null=False, on_delete=models.CASCADE)
    offered_on = models.DateTimeField(
        verbose_name=_("Date offered"), auto_now_add=timezone.now)
    accepted_on = models.DateTimeField(
        verbose_name=_("Date accepted"), blank=True, null=True)
    declined_on = models.DateTimeField(
        verbose_name=_("Date declined"), blank=True, null=True)

    objects = models.Manager()
    accepted = AcceptedManager()

    class Meta:
        verbose_name = _("User badge")
        verbose_name_plural = _("User badges")
        unique_together = ("badge_type", "user")


@receiver(models.signals.post_save, sender=StoryRead)
def create_badge_offer(sender, **kwargs):
    # TODO
    print("Someone read a story...")
