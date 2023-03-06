from dash.orgs.views import OrgPermsMixin, OrgObjPermsMixin
from django.shortcuts import render
from smartmin.views import (
    SmartCRUDL,
    SmartListView,
    SmartUpdateView,
    SmartCreateView,
)
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from ureport.userbadges.forms import BadgeTypeForm
from ureport.userbadges.serializers import (
    BadgeTypeSerializer,
    UserBadgeSerializer,
)
from ureport.userbadges.models import BadgeType
   

class BadgeTypeCRUDL(SmartCRUDL):
    model = BadgeType
    actions = ("create", "update", "list")

    class Update(OrgObjPermsMixin, SmartUpdateView):
        form_class = BadgeTypeForm
        fields = (
            "title", "image", "description", "is_visible", 
            "item_type", "item_category", "item_count",
        )

    class Create(OrgPermsMixin, SmartCreateView):
        form_class = BadgeTypeForm
        fields = (
            "org", "title", "image", "description", "item_type",
        )

    class List(OrgPermsMixin, SmartListView):
        fields = (
            "org", "title", "item_type", "is_visible", 
        )
        ordering = ("org__name", "title")

        def get_queryset(self, **kwargs):
            queryset = super(BadgeTypeCRUDL.List, self).get_queryset(**kwargs)

            if self.derive_org():
                queryset = queryset.filter(org=self.derive_org())

            return queryset
