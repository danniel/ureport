from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied

from ureport.apiextras.views import (
    IsOwnerUserOrAdmin,
    USER_API_PATH, 
)
from ureport.storyextras.models import (
    StoryBookmark, 
    StoryRating, 
    StoryRead, 
    StoryReward,
)
from ureport.storyextras.serializers import (
    StoryBookmarkSerializer,
    StoryRatingSerializer,
    StoryReadActionSerializer,
    StoryRewardSerializer,
)
from ureport.userbadges.models import create_badge_for_story
from ureport.userbadges.serializers import UserBadgeSerializer


class StoryBookmarkViewSet(ModelViewSet):
    """
    This endpoint allows you to manage the story bookmarks.

    ## Listing story bookmarks

    By making a ```GET``` request you can list all the story bookmarks for all organizations, filtering them as needed.
    
    ### Query filters:

    * **user** - the ID of the user that set the bookmark (int)
    * **story** - the ID of the story for which the bookmark was set (int)

    Each story bookmark has the following attributes:

    * **id** - the ID of the item (int)
    * **user** - the ID of the user that set the bookmark (int)
    * **story** - the ID of the story for which the bookmark was set (int)

    Example:

        GET /api/v1/storybookmarks/

    Response is the list of story bookmarks for all organizations, most recent first:

        {
            "count": 389,
            "next": "/api/v1/storybookmarks/?page=2",
            "previous": null,
            "results": [
            {
                "id": 1,
                "user": 7,
                "story": 434
            },
            ...
        }
    """
    
    serializer_class = StoryBookmarkSerializer
    queryset = StoryBookmark.objects.all()
    model = StoryBookmark
    permission_classes = [IsOwnerUserOrAdmin]

    def filter_queryset(self, queryset):
        user_id = self.request.query_params.get("user")
        story_id = self.request.query_params.get("story")
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if story_id:
            queryset = queryset.filter(story_id=story_id)

        return queryset

    @action(detail=False, methods=['get'], url_path=USER_API_PATH)
    def retrieve_user_bookmarks(self, request, user_id):
        """
        Get the bookmarks for the current user
        """

        queryset = self.model.objects.filter(user_id=user_id)
        filtered_queryset = self.filter_queryset(queryset)
        serializer = StoryBookmarkSerializer(filtered_queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'], url_path=USER_API_PATH)
    def remove_user_bookmarks(self, request, user_id):
        """
        Remove any bookmarks of the current user
        """

        count = StoryBookmark.objects.filter(
            story_id=request.data.get("story"),
            user_id=user_id
        ).delete()
        return Response({"count": count[0]})

    @action(detail=False, methods=['post'], url_path=USER_API_PATH)
    def create_user_bookmark(self, request, user_id):
        """
        Bookmark a story for the current user
        """

        data = {
            'story': request.data.get("story"),
            'user': user_id,
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
    permission_classes = [IsOwnerUserOrAdmin]

    def filter_queryset(self, queryset):
        user_id = self.request.query_params.get("user")
        story_id = self.request.query_params.get("story")
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if story_id:
            queryset = queryset.filter(story_id=story_id)

        return queryset

    @action(detail=False, methods=['get'], url_path=USER_API_PATH)
    def retrieve_user_ratings(self, request, user_id):
        """
        Get the ratings given by the current user
        """
        queryset = self.model.objects.filter(user_id=user_id)
        filtered_queryset = self.filter_queryset(queryset)
        serializer = StoryRatingSerializer(filtered_queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], url_path=USER_API_PATH)
    def set_user_rating(self, request, user_id):
        """
        Create or update a rating given by the current user
        """
        data = {
            'user': user_id,
            'story': request.data.get("story"),
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)


class StoryReadActionViewSet(ModelViewSet):
    """
    This endpoint allows you to manage the story read actions


    Query filters:

    * **user** - the ID of the user that read the story (int)
    * **story** - the ID of the story which was read by the user (int)

    """
    
    serializer_class = StoryReadActionSerializer
    queryset = StoryRead.objects.all()
    model = StoryRead
    permission_classes = [IsOwnerUserOrAdmin]

    def filter_queryset(self, queryset):
        user_id = self.request.query_params.get("user")
        story_id = self.request.query_params.get("story")
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if story_id:
            queryset = queryset.filter(story_id=story_id)

        return queryset

    @action(detail=False, methods=['get'], url_path=USER_API_PATH)
    def retrieve_user_reads(self, request, user_id):
        """
        Get the story reads by the current user
        """
        
        queryset = self.model.objects.filter(user_id=user_id)
        filtered_queryset = self.filter_queryset(queryset)
        serializer = StoryReadActionSerializer(filtered_queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], url_path=USER_API_PATH)
    def set_user_read(self, request, user_id):
        """
        Mark a story as read by the current user and return any earned badges
        """
        
        data = {
            'story': request.data.get("story"),
            'user': user_id,
        }
        serializer = StoryReadActionSerializer(data=data)

        if serializer.is_valid():
            read = serializer.save()

            # Count how many stories the user has read
            total_reads = StoryRead.objects.filter(
                user=read.user, story__org=read.story.org).count()
            category_reads = StoryRead.objects.filter(
                user=read.user, story__category=read.story.category).count()

            new_badges = create_badge_for_story(
                read.user, read.story.org, read.story.category, total_reads, category_reads)

            # show the new badges
            badges_serializer = UserBadgeSerializer(new_badges, many=True)
            return Response(badges_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StoryRewardViewSet(ModelViewSet):
    """
    This endpoint allows you to manage the story rewards


    Query filters:

    * **user** - the ID of the user that received the reward (int)
    * **story** - the ID of the story for which the reward was given (int)

    """
    
    serializer_class = StoryRewardSerializer
    queryset = StoryReward.objects.all()
    model = StoryReward
    permission_classes = [IsOwnerUserOrAdmin]

    def filter_queryset(self, queryset):
        user_id = self.request.query_params.get("user")
        story_id = self.request.query_params.get("story")
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if story_id:
            queryset = queryset.filter(story_id=story_id)

        return queryset

    @action(detail=False, methods=['get'], url_path=USER_API_PATH)
    def retrieve_user_rewards(self, request, user_id):
        """
        Get the rewards received by the current user
        """
        
        queryset = self.model.objects.filter(user_id=user_id)
        filtered_queryset = self.filter_queryset(queryset)
        serializer = StoryRewardSerializer(filtered_queryset, many=True)
        return Response(serializer.data)
