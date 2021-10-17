import django_filters
from .models import CustomUser

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'gender']

        first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='startswith')
        second_name = django_filters.CharFilter(field_name='second_name', lookup_expr='startswith')
        gender = django_filters.CharFilter(field_name='gender', lookup_expr='exact')
