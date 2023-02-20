from rest_framework import serializers

from ureport.userprofiles.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("user", "contact_uuid", "image", )
