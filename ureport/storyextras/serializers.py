from rest_framework import serializers

from ureport.api.serializers import StoryShortReadSerializer
from ureport.storyextras.models import (
    StoryBookmark, 
    StoryRating, 
    StoryRead, 
    StoryReward,
    StorySettings,
)


class StorySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorySettings
        fields = ("display_rating", "rating", )


class StoryBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryBookmark
        fields = ("id", "user", "story", )


class StoryBookmarkDetailedSerializer(StoryBookmarkSerializer):
    story = StoryShortReadSerializer()

    class Meta:
        model = StoryBookmark
        fields = ("id", "user", "story", )


class StoryRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryRating
        fields = ("id", "user", "score", "story", )


class StoryRatingDetailedSerializer(StoryRatingSerializer):
    story = StoryShortReadSerializer()

    class Meta:
        model = StoryRating
        fields = ("id", "user", "score", "story", )


class StoryReadActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryRead
        fields = ("id", "user", "story", )


class StoryReadActionDetailedSerializer(StoryReadActionSerializer):
    story = StoryShortReadSerializer()

    class Meta:
        model = StoryRead
        fields = ("id", "user", "story", )


class StoryRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryReward
        fields = ("id", "user", "points", "story", )


class StoryRewardDetailedSerializer(StoryRewardSerializer):
    story = StoryShortReadSerializer()

    class Meta:
        model = StoryReward
        fields = ("id", "user", "points", "story", )
