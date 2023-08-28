from django_filters import FilterSet
from .models import Advertsement, Replies

class RepliesFilter(FilterSet):
    class Meta:
        model = Replies
        fields = (
            'body',
            'advertsement',
            'user'
        )