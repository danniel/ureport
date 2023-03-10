from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ureport.userprofiles.serializers import UserProfileSerializer, CreateUserSerializer


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

