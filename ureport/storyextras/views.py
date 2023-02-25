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
    StoryRatingForStorySerializer,
    StoryRatingForUserSerializer,
    StoryReadActionSerializer,
    StoryRewardSerializer,
)


class StoryBookmarkViewSet(ModelViewSet):
    """
    This endpoint allows you to manage the story bookmarks


    Query filters:

    * **user** - the ID of the user that set the bookmark (int)
    * **story** - the ID of the story for which the bookmark was set (int)

    """
    
    serializer_class = StoryBookmarkSerializer
    queryset = StoryBookmark.objects.all()
    model = StoryBookmark
    # TODO: permissions
    # permission_classes = []

    def filter_queryset(self, queryset):
        params = self.request.query_params

        user_id = params.get("user")
        story_id = params.get("story")
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if story_id:
            queryset = queryset.filter(story_id=story_id)

        return queryset

    # @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[\d]+)')
    # def list_for_user(self, request, user_id):
    #     """
    #     List all bookmarked stories for the user id specified in URL
    #     """
    #     queryset = self.model.objects.filter(user_id=user_id)
    #     serializer_context = {"request": request}
    #     serializer = StoryBookmarkForUserSerializer(queryset, many=True, context=serializer_context)
    #     return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='story/(?P<story_id>[\d]+)')
    def list_for_story(self, request, story_id):
        """
        List all bookmark users for the story id specified in URL
        """
        queryset = self.model.objects.filter(story_id=story_id)
        serializer = StoryBookmarkForStorySerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'], url_path='story/(?P<story_id>[\d]+)')
    def remove_bookmark(self, request, story_id):
        """
        Remove any bookmarks for the current story for the authenticated user
        """
        count = StoryBookmark.objects.filter(
            story_id=story_id,
            user_id=request.user.id
        ).delete()
        return Response({"count": count[0]})

    @action(detail=False, methods=['post'], url_path='story/(?P<story_id>[\d]+)')
    def create_bookmark(self, request, story_id):
        """
        Bookmark the current story for the authenticated user
        """
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


class StoryRatingViewSet(ModelViewSet):
    """
    This endpoint allows you to manage the story ratings


    Query filters:

    * **user** - the ID of the user that set the rating (int)
    * **story** - the ID of the story for which the rating was set (int)

    """
    
    serializer_class = StoryRatingSerializer
    queryset = StoryRating.objects.all()
    model = StoryRating
    # TODO: permissions
    # permission_classes = []

    def filter_queryset(self, queryset):
        params = self.request.query_params

        user_id = params.get("user")
        story_id = params.get("story")
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if story_id:
            queryset = queryset.filter(story_id=story_id)

        return queryset

    # @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[\d]+)')
    # def list_for_user(self, request, user_id):
    #     """
    #     List all rated stories for the user id specified in URL
    #     """
    #     queryset = self.model.objects.filter(user_id=user_id)
    #     serializer_context = {"request": request}
    #     serializer = StoryRatingForUserSerializer(queryset, many=True, context=serializer_context)
    #     return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='story/(?P<story_id>[\d]+)')
    def list_for_story(self, request, story_id):
        """
        List all users who rated the story id specified in URL
        """
        queryset = self.model.objects.filter(story_id=story_id)
        serializer = StoryRatingForStorySerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='story/(?P<story_id>[\d]+)')
    def set_rating(self, request, story_id):
        """
        Create or update the rating of the current story for the authenticated user
        """
        data = {
            'story': story_id,
            'user': request.user.id,
            'score': request.data.get("score"),
        }

        try:
            rating = StoryRating.objects.get(
                user=data["user"],
                story=data["story"],
            )
            serializer = StoryRatingSerializer(rating, data=data, partial=True)
            created = False
        except StoryRating.DoesNotExist:
            serializer = StoryRatingSerializer(data=data)
            created = True

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if created:
            return Response(StoryRatingSerializer(rating).data, status=status.HTTP_201_CREATED)
        else:
            return Response(StoryRatingSerializer(rating).data, status=status.HTTP_200_OK)
