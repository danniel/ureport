from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from ureport.userprofiles.serializers import UserProfileSerializer

