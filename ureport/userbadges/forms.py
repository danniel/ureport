from django import forms
from ureport.userbadges.models import BadgeType


class BadgeTypeForm(forms.ModelForm):

    class Meta:
        model = BadgeType
        fields = (
            "org", "title", "image", "description", "is_visible", 
            "item_type", "item_category", "item_count",
        )
