from rest_framework import serializers

from ureport.storyextras.models import (
    StoryBookmark, 
    StoryRating, 
    StoryRead, 
    StoryReward,
)


class StoryBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryBookmark
        fields = ("story", "user", )


class StoryRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryRating
        fields = ("story", "user", "score", )


class StoryReadActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryRead
        fields = ("story", "user", )


class StoryRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryReward
        fields = ("story", "user", "points", )
