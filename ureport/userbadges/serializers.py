from rest_framework import serializers

from ureport.userbadges.models import BadgeType, UserBadge


class BadgeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BadgeType
        fields = ("id", "org", "title", "image", "description", "item_category", )


class UserBadgeSerializer(serializers.ModelSerializer):
    badge_type = BadgeTypeSerializer()

    class Meta:
        model = UserBadge
        fields = ("id", "badge_type", "user", "offered_on", "accepted_on", "declined_on")


class UserBadgeAcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBadge
        fields = ("id", "accepted_on", "declined_on")
