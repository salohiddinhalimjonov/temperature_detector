import django_filters
from .models import AboutUrl

class ChoiceFilter(django_filters.FilterSet):
    class Meta:
        model = AboutUrl
        fields = ['choices']