from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ureport.apiextras.views import IsOwnerUserOrAdmin
from ureport.userprofiles.serializers import (
    UserProfileSerializer, 
    CreateUserSerializer,
    ChangePasswordSerializer,
)


@api_view(["POST"])
def create_user(request):
    serializer = CreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = Token.objects.get_or_create(user=user)[0]
    return Response({
        "id": user.id,
        "token": token.key,
    })


@api_view(["POST"])
@permission_classes([IsOwnerUserOrAdmin])
def change_password(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404

    serializer = ChangePasswordSerializer(instance=user, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({})
