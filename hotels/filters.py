from .models import Hotel

from django_filters import rest_framework as filters
from rest_framework import filters as OrderFilters
from django.db.models import Min

class HotelFilter(filters.FilterSet):
    check_in = filters.DateFilter(field_name='reservations__check_in', lookup_expr='lte')
    check_out = filters.DateFilter(field_name='reservations__check_out', lookup_expr='gte')
    price_range = filters.RangeFilter(field_name='rooms__price')
    stars = filters.NumberFilter(field_name='stars')

    class Meta:
        model = Hotel
        fields = ['check_in', 'check_out', 'price_range', 'stars']


class HotelMinRoomOrder(OrderFilters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.annotate(min_room_price=Min('rooms__price'))