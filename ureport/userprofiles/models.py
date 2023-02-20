from functools import partial

from dash.utils import generate_file_path
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserProfile(models.Model):
    """
    This class links an Ureport user account to a RapidPro contact
    based on the RapidPro UUID.
    """

    user = models.OneToOneField(
        User, verbose_name=_("User"), blank=False, null=False, on_delete=models.CASCADE,
        primary_key=True)
    
    # We do not use a ForeignKey because there can be several "Contacts" with
    # the same imported UUID but assigned to different Orgs
    contact_uuid = models.CharField(
        verbose_name=_("Contact UUID"), max_length=36, blank=True, null=False, default="",
        db_index=True)

    image = models.ImageField(
        verbose_name=_("Image"), 
        upload_to=partial(generate_file_path, "userprofiles"), 
        help_text=_("The profile image file to use"))

    password_reset_code = models.CharField(
        verbose_name=_("Confirmation code"), 
        max_length=8, blank=True, null=False, default="",
        help_text=_("Confirmation code for the password reset"))

    password_reset_expiry = models.DateTimeField(
        verbose_name=_("Expiration date"), blank=True, null=True,
        help_text=_("Expiration date for the password reset"))

    class Meta:
        verbose_name = _("User profile")
        verbose_name_plural = _("Use profiles")