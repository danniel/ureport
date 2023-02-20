from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ureport.storyextras.models import (
    StoryBookmark, 
    StoryRating, 
    StoryRead, 
    StoryReward,
)
from ureport.storyextras.serializers import (
    StoryBookmarkForStorySerializer,
    StoryBookmarkForUserSerializer,
    StoryBookmarkSerializer,
    StoryRatingSerializer,
    StoryReadActionSerializer,
    StoryRewardSerializer,
)


class StoryBookmarkViewSet(ModelViewSet):
    """
    This endpoint allows you to manage the story bookmarks

    """
    
    serializer_class = StoryBookmarkSerializer
    queryset = StoryBookmark.objects.all()
    model = StoryBookmark
    # TODO: permissions
    # permission_classes = []

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[\d]+)')
    def list_for_user(self, request, user_id):
        queryset = self.model.objects.filter(user_id=user_id)
        serializer_context = {"request": request}
        serializer = StoryBookmarkForUserSerializer(queryset, many=True, context=serializer_context)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='story/(?P<story_id>[\d]+)')
    def list_for_story(self, request, story_id):
        queryset = self.model.objects.filter(story_id=story_id)
        serializer = StoryBookmarkForStorySerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'], url_path='story/(?P<story_id>[\d]+)')
    def remove_bookmark(self, request, story_id):
        count = StoryBookmark.objects.filter(
            story_id=story_id,
            user_id=request.user.id
        ).delete()
        return Response({"count": count[0]})

    @action(detail=False, methods=['post'], url_path='story/(?P<story_id>[\d]+)')
    def create_bookmark(self, request, story_id):
        data = {
            'story': story_id,
            'user': request.user.id,
        }
        serializer = StoryBookmarkSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

