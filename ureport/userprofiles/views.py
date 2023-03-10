from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.authtoken.models import Token
from rest_framework import decorators
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ureport.apiextras.views import (
    IsOwnerUserOrAdmin,
    USER_API_PATH
)
from ureport.userprofiles.serializers import (
    UserWithProfileSerializer,
    UserProfileSerializer, 
    CreateUserSerializer,
    ChangePasswordSerializer,
)


@decorators.api_view(["POST"])
def create_user(request):
    serializer = CreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = Token.objects.get_or_create(user=user)[0]
    return Response({
        "id": user.id,
        "token": token.key,
    })


@decorators.api_view(["POST"])
@decorators.permission_classes([IsOwnerUserOrAdmin])
def change_password(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404

    serializer = ChangePasswordSerializer(instance=user, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({})


class UserViewSet(ModelViewSet):
    """
    """
    
    serializer_class = UserWithProfileSerializer
    queryset = User.objects.all()
    model = User
    permission_classes = [IsOwnerUserOrAdmin]

    @decorators.action(detail=False, methods=['get'], url_path=USER_API_PATH)
    def retrieve_user_with_profile(self, request, user_id):
        """
        TODO: flatten the response object
        """
        queryset = self.get_queryset().filter(id=user_id).get()
        serializer = UserWithProfileSerializer(queryset, many=False)
        return Response(serializer.data)
