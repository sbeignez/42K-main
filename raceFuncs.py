import django_filters
from django_tables2 import tables

from app.models import RaceEvent


class RaceFilter(django_filters.FilterSet):
    country = django_filters.ModelChoiceFilter(queryset=RaceEvent.objects.values_list('country', flat=True), to_field_name='country')
    date = django_filters.DateRangeFilter()
    class Meta:
        model = RaceEvent
        fields = { 'country',
                   'date'
                 }


class RaceTable(tables.Table):
    class Meta:
        model = RaceEvent
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        fields = ('date', 'name', 'city', 'country') # fields to display
