# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from rest_framework_swagger.views import get_swagger_view

from django.urls import re_path
from django.views.generic import RedirectView

from ureport.api.views import (
    CategoryDetails,
    CategoryList,
    DashBlockDetails,
    DashBlockList,
    FeaturedPollList,
    ImageDetails,
    ImageList,
    NewsItemDetails,
    NewsItemList,
    OrgDetails,
    OrgList,
    PollDetails,
    PollList,
    StoryDetails,
    StoryList,
    VideoDetails,
    VideoList,
)
from ureport.storyextras.views import (
    StoryBookmarkViewSet,
    StoryRatingViewSet,
    StoryReadActionViewSet,
    StoryRewardViewSet,
)
from ureport.userbadges.views import UserBadgeViewSet


schema_view = get_swagger_view(title="API")


urlpatterns = [
    re_path(r"^$", RedirectView.as_view(pattern_name="api.v1.docs", permanent=False), name="api.v1"),
    re_path(r"^docs/", schema_view, name="api.v1.docs"),
    re_path(r"^orgs/$", OrgList.as_view(), name="api.v1.org_list"),
    re_path(r"^orgs/(?P<pk>[\d]+)/$", OrgDetails.as_view(), name="api.v1.org_details"),
    re_path(r"^polls/org/(?P<org>[\d]+)/$", PollList.as_view(), name="api.v1.org_poll_list"),
    re_path(r"^polls/org/(?P<org>[\d]+)/featured/$", FeaturedPollList.as_view(), name="api.v1.org_poll_fetured"),
    re_path(r"^polls/(?P<pk>[\d]+)/$", PollDetails.as_view(), name="api.v1.poll_details"),
    re_path(r"^news/org/(?P<org>[\d]+)/$", NewsItemList.as_view(), name="api.v1.org_newsitem_list"),
    re_path(r"^news/(?P<pk>[\d]+)/$", NewsItemDetails.as_view(), name="api.v1.newsitem_details"),
    re_path(r"^videos/org/(?P<org>[\d]+)/$", VideoList.as_view(), name="api.v1.org_video_list"),
    re_path(r"^videos/(?P<pk>[\d]+)/$", VideoDetails.as_view(), name="api.v1.video_details"),
    re_path(r"^assets/org/(?P<org>[\d]+)/$", ImageList.as_view(), name="api.v1.org_asset_list"),
    re_path(r"^assets/(?P<pk>[\d]+)/$", ImageDetails.as_view(), name="api.v1.asset_details"),
    re_path(r"^dashblocks/org/(?P<org>[\d]+)/$", DashBlockList.as_view(), name="api.v1.org_dashblock_list"),
    re_path(r"^dashblocks/(?P<pk>[\d]+)/$", DashBlockDetails.as_view(), name="api.v1.dashblock_details"),
    re_path(r"^stories/org/(?P<org>[\d]+)/$", StoryList.as_view(), name="api.v1.org_story_list"),
    re_path(r"^stories/(?P<pk>[\d]+)/$", StoryDetails.as_view(), name="api.v1.story_details"),
    
    # Categories API extension:
    re_path(r"^categories/org/(?P<org>[\d]+)/$", CategoryList.as_view(), name="api.v1.org_category_list"),
    re_path(r"^categories/(?P<pk>[\d]+)/$", CategoryDetails.as_view(), name="api.v1.category_details"),

    # StoryBookmarks API
    re_path(
        r"^storybookmarks/$", 
        StoryBookmarkViewSet.as_view({
            "get": "list", 
            "post": "create",
        }), 
        name="api.v1.storybookmarks_list"
    ),
    re_path(
        r"^storybookmarks/(?P<pk>[\d]+)/$", 
        StoryBookmarkViewSet.as_view({
            "get": "retrieve",
            # "put": "update",
            # "patch": "partial_update",
            "delete": "destroy",
        }), 
        name="api.v1.storybookmarks_detail"
    ),
    re_path(
        r"^storybookmarks/user/(?P<user_id>[\d]+)/$", 
        StoryBookmarkViewSet.as_view({
            "get": "retrieve_user_bookmarks",
            "post": "create_user_bookmark",
            "delete": "remove_user_bookmarks",
        }), 
        name="api.v1.storybookmarks_for_user"
    ),

    # StoryRatings API
    re_path(
        r"^storyratings/$", 
        StoryRatingViewSet.as_view({
            "get": "list", 
            "post": "create",
        }), 
        name="api.v1.storyratings_list"
    ),
    re_path(
        r"^storyratings/(?P<pk>[\d]+)/$", 
        StoryRatingViewSet.as_view({
            "get": "retrieve",
            # "put": "update",
            # "patch": "partial_update",
            "delete": "destroy",
        }), 
        name="api.v1.storyratings_detail"
    ),
    re_path(
        r"^storyratings/user/(?P<user_id>[\d]+)/$",
        StoryRatingViewSet.as_view({
            "get": "retrieve_user_ratings",
            "post": "set_user_rating",
        }), 
        name="api.v1.storyratings_for_user"
    ),

    # StoryReads API
    re_path(
        r"^storyreads/$", 
        StoryReadActionViewSet.as_view({
            "get": "list", 
            "post": "create",
        }), 
        name="api.v1.storyreads_list"
    ),
    re_path(
        r"^storyreads/(?P<pk>[\d]+)/$", 
        StoryReadActionViewSet.as_view({
            "get": "retrieve",
            # "put": "update",
            # "patch": "partial_update",
            "delete": "destroy",
        }), 
        name="api.v1.storyreads_detail"
    ),
    re_path(
        r"^storyreads/user/(?P<user_id>[\d]+)/$",
        StoryReadActionViewSet.as_view({
            "get": "retrieve_user_reads",
            "post": "set_user_read",
        }), 
        name="api.v1.storyreads_for_user"
    ),

    # StoryRewards API
    re_path(
        r"^storyrewards/$", 
        StoryRewardViewSet.as_view({
            "get": "list", 
            "post": "create",
        }), 
        name="api.v1.storyrewards_list"
    ),
    re_path(
        r"^storyrewards/(?P<pk>[\d]+)/$", 
        StoryRewardViewSet.as_view({
            "get": "retrieve",
            # "put": "update",
            # "patch": "partial_update",
            "delete": "destroy",
        }), 
        name="api.v1.storyrewards_detail"
    ),
    re_path(
        r"^storyrewards/user/(?P<user_id>[\d]+)/$",
        StoryRewardViewSet.as_view({
            "get": "retrieve_user_rewards",
        }), 
        name="api.v1.storyrewards_for_user"
    ),

    # UserBadges API
    re_path(
        r"^userbadges/$", 
        UserBadgeViewSet.as_view({
            "get": "list", 
            "post": "create",
        }), 
        name="api.v1.userbadges_list"
    ),
    re_path(
        r"^userbadges/(?P<pk>[\d]+)/$", 
        UserBadgeViewSet.as_view({
            "get": "retrieve",
            # "put": "update",
            # "patch": "partial_update",
            "delete": "destroy",
        }), 
        name="api.v1.userbadges_detail"
    ),
    re_path(
        r"^userbadges/user/(?P<user_id>[\d]+)/$",
        UserBadgeViewSet.as_view({
            "get": "retrieve_user_badges",
        }), 
        name="api.v1.userbadges_for_user"
    ),
]
