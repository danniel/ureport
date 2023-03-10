from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ureport.userprofiles.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("user", "contact_uuid", "image", )


class CreateUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(max_length=128)

    class Meta:
        model = User
        fields = ("full_name", "email", "password")

    def validate_email(self, value):
        clean_email = value.strip()        
        if len(clean_email.split("@")) != 2:
            raise serializers.ValidationError(_("Wrong email format"))

        exists = User.objects.filter(username__iexact=clean_email).count()
        if exists:
            raise serializers.ValidationError(_("Email address already used"))
        else:
            return clean_email

    def create(self, validated_data):
        split_name = validated_data["full_name"].split(" ")
        
        first_name = split_name[0]
        if len(split_name) > 1:
            last_name = split_name[1]

        user = User(
            email=validated_data["email"],
            username=validated_data["email"],
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
