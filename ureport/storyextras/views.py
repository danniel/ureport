from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied

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


USER_API_PATH = "user/(?P<user_id>[\d]+)"
STORY_API_PATH = "story/(?P<story_id>[\d]+)"
USER_STORY_API_PATH = "{}/{}".format(USER_API_PATH, STORY_API_PATH)


class IsOwnerUserOrAdmin(IsAuthenticated):
    """
    Only allow staff members or authenticated users who own the object
    """
    def has_permission(self, request, view):
        """
        For non-staff, check that the URL user is the same as the authenticated user
        """
        
        try:
            url_user_id = int(view.kwargs.get("user_id", 0))
        except ValueError:
            url_user_id = None

        if request.user.is_staff or url_user_id == request.user.id:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        """
        For non-staff, check that the object owner user is the same as the authenticated user
        """
        if request.user.is_staff or obj.user == request.user:
            return True
        else:
            return False


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

        queryset = self.filter_queryset(self.model.objects.filter(user_id=user_id))
        serializer = StoryBookmarkSerializer(queryset, many=True)
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
        Create or update the rating of the current story for the current user
        """
        queryset = self.filter_queryset(self.model.objects.filter(user_id=user_id))
        serializer = StoryRatingSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], url_path=USER_API_PATH)
    def set_user_rating(self, request, user_id):
        """
        Create or update the rating of the current story for the current user
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

    * **user** - the ID of the user that set the rating (int)
    * **story** - the ID of the story for which the rating was set (int)

    """
    
    serializer_class = StoryReadActionSerializer
    queryset = StoryRating.objects.all()
    model = StoryRead
    permission_classes = [IsOwnerUserOrAdmin]

    def filter_queryset(self, queryset):
        params = self.request.query_params

        user_id = params.get("user")
        story_id = params.get("story")
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if story_id:
            queryset = queryset.filter(story_id=story_id)

        return queryset

    @action(detail=False, methods=['get'], url_path=USER_API_PATH)
    def user_ratings(self, request, user_id):
        """
        Create or update the rating of the current story for the current user
        """
        queryset = self.model.objects.filter(story_id=story_id, user_id=user_id)
        serializer = StoryRatingSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], url_path=USER_API_PATH)
    def set_rating(self, request, user_id):
        """
        Create or update the rating of the current story for the current user
        """
        data = {
            'story': story_id,
            'user': user_id,
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
