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


class StoryBookmarkForStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryBookmark
        fields = ("user", )


class StoryBookmarkForUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StoryBookmark
        fields = ("story", )
        extra_kwargs = {
            "story": {"lookup_field": "pk", "view_name": "api.v1.story_details"}
        }


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
