from rest_framework import serializers

from ureport.userbadges.models import BadgeType, UserBadge


class BadgeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BadgeType
        fields = ("org", "title", "image", "description", "item_category", )


class UserBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBadge
        fields = ("badge_type", "user", "offered_on", "accepted_on", )
