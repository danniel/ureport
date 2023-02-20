from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.generics import (
    ListAPIView, 
    ListCreateAPIView, 
    RetrieveAPIView,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from ureport.storyextras.serializers import (
    StoryBookmarkSerializer,
    StoryBookmarkForUserSerializer,
    StoryRatingSerializer,
    StoryReadActionSerializer,
    StoryRewardSerializer,
)
from ureport.storyextras.models import (
    StoryBookmark, 
    StoryRating,
    StoryRead,
    StoryReward,
)


class PerUserListAPIView(ListAPIView):
    def get_queryset(self):
        q = self.model.objects.filter(user_id=self.kwargs.get("user"))
        return q


class PerStoryListCreateAPIView(ListCreateAPIView):
    # permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        q = self.model.objects.filter(story_id=self.kwargs.get("story"))
        return q


class UserStoryBookmarkList(PerUserListAPIView):
    """
    This endpoint allows you to list the bookmarks of an user.

    ## Listing story bookmarks

    By making a ```GET``` request you can list all the bookmarks for an user

    Example:

        GET /api/v1/storybookmarks/user/1/

    """
    
    serializer_class = StoryBookmarkSerializer
    model = StoryBookmark


class StoryBookmarkList(PerStoryListCreateAPIView):
    """
    This endpoint allows you to list the bookmarks of a story.

    ## Listing story bookmarks

    By making a ```GET``` request you can list all the bookmarks for a story

    Example:

        GET /api/v1/storybookmarks/story/1/


    ## Creating story bookmarks

    By making a ```POST``` request you can add a story bookmark for the current user

    Example:

        POST /api/v1/storybookmarks/story/1/

    """
    
    serializer_class = StoryBookmarkForUserSerializer
    model = StoryBookmark

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



# @action(detail=True, methods=['get'])
# def bookmarks(self, request):
#     story = self.get_object()
#     bmarks = StoryBookmark.objects.filter(story=story).all()
#     page = self.paginate_queryset(bmarks)
#     if page is not None:
#         serializer = StoryBookmarkSerializer(page, many=True)
#         return self.get_paginated_response(serializer.data)

#     serializer = StoryBookmarkSerializer(bmarks, many=True)
#     return Response(serializer.data)
