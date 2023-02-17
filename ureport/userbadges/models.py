from dash.categories.models import Category
from dash.orgs.models import Org
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class BadgeType(models.Model):
    org = models.ForeignKey(Org, blank=False, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=250, blank=True, null=False, default="")
    is_visible = models.BooleanField(default=True, db_index=True)
    # TODO: per category read count
    # TODO: per poll

    class Meta:
        unique_together = ("org", "title")


class UserBadge(models.Model):
    badge_type = models.ForeignKey(BadgeType, blank=False, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    received_on = models.DateTimeField(auto_now_add=timezone.now)

    class Meta:
        unique_together = ("badge_type", "user")